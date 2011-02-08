window.addEventListener("load", function() { DetikLangsung.init(); }, false);

var DetikLangsung = {
    //PARAM
    exact_matches:        ["http://us.detik.com/", "http://www.detik.com/"],
    beginwith_matches:    ["http://us.detik.com/?","http://www.detik.com/?"],
    DEBUG: true,
    signaturedl:  "Detik Langsung melangsungkan link ini!",
    p_su:         /\.com($|\/(sepakbola)?\??[^\/]*$)/,
    block1:       /(tv|suarapembaca)\.detik\.com\/.*$/,
    block2:       /\.com\/(infoanda|beritaterpopuler|video|indeks)\??[^\/]*$/,
    ulinks:       [],   //array of references to <a> that needs resolving
  
    PRELOADING:         true,//true enables early lookup of all short links
    preloading_delay:   1000,//time to wait before preloading starts (in order to not compete with loading images of main page)
    cached_title_url:   {}, //list of titles with their real links
    queue_resolving:    {}, //list of portal links that's awaiting for retrieval
    resolved_titles:    {}, //collection of news that's been looked-up before (used to avoid lookup revisiting)
    jobcounter:         0,
    utimer:             null,  //refers to timer that will clear the state
    instance_counter:   0,     //keep count of instance running
    unload_delay:       600000,   //clear cache x milisecond after user left main page. 10 minutes is a good balance.

    //======FIREFOX EXTENSION SPECIFIC=======
    doc:null,
  init: function() {
    var appcontent = document.getElementById("appcontent");   // browser
    if(appcontent)
        appcontent.addEventListener("DOMContentLoaded", function(event) { DetikLangsung.onPageLoad(event) }, true);
  },
  
  page_matches: function(url) {
    for (var key in this.exact_matches)
        if (url == this.exact_matches[key]) return true;
    for (var key in this.beginwith_matches)
        if (url.substr(0, this.beginwith_matches[key].length) == this.beginwith_matches[key]) return true;
    return false;
  },
  
  onPageLoad: function(event) {
    var doc = event.originalTarget; // doc is document that triggered "onload" event
    if(event.originalTarget.nodeName == "#document"  && this.page_matches(doc.location.href)) {
        this.doc = doc;
        clearTimeout(this.utimer);
        this.init_extension();
    }
    this.instance_counter++;
    event.originalTarget.defaultView.addEventListener("unload", function(event){ DetikLangsung.onPageUnload(event); }, true);
  },
  
  onPageUnload: function(event) {
    DetikLangsung.ulinks = [];
    //clear cache and all states after certain duration to conserve browser's memory
    this.instance_counter--;
    if (this.instance_counter == 0) {
        this.utimer = setTimeout(
            function() {DetikLangsung.log("Unloading Detik Langsung");DetikLangsung.cached_title_url = {};DetikLangsung.resolved_titles = {};},
            DetikLangsung.unload_delay);
    }
  },
  
  log: function (msg) {if (this.DEBUG) Components.utils.reportError(msg);},

  init_extension: function() {
    this.log("Init at URL " + this.doc.location.href);
    this.solve_same_page();
    this.log("Solving " + this.ulinks.length + " remaining links");
    this.solve_cache();
    this.solve_remaining_links_cb(true);
  },
  
  solve_same_page: function() {
    //first pass, collect all news links with "real" urls (used later), and short urls (ones that needs resolving)
    var real_link_title = {};
    var short_link = [];
    var anchors = this.doc.getElementsByTagName("a");
    for (var i=0;i<anchors.length;i++) {
        var link = anchors[i];
        var title = link.textContent;
        var href = link.href;
        if (title.length > 12 && href.search(this.p_su) == -1 ) {
            real_link_title[title] = href;
            continue;
        }
        if (title.length > 12 && link.host != 'twitter.com' && link.target != "_blank" && 
            href.search(this.p_su) > -1 && link.parentNode.className != "hnews" &&
            href.search(this.block1) == -1 && href.search(this.block2) == -1) { 
            short_link.push(link);
        }
    }
    //second pass, solve short links
    for (var i=0;i < short_link.length; i++) {
        var link = short_link[i];
        var title = link.textContent;
        if (title in real_link_title) {
            link.href = real_link_title[title];
            link.title = this.signaturedl; 
            continue;
        }
        if (!this.PRELOADING) link.title = "Detik Langsung will resolve this link";
        this.ulinks.push(link);
    }
  },
  
  solve_cache: function() {
    for (var i=this.ulinks.length-1; i>=0; i--) {
        var link = this.ulinks[i];
        var title = link.textContent;
        var trimmed_title = this.trim(title);
        if (trimmed_title in this.cached_title_url) {
            link.href = this.cached_title_url[trimmed_title];
            link.title = this.signaturedl;
            link.removeEventListener("click", DetikLangsung.link_clicked, false);
            this.ulinks.splice(i,1);
            continue;
        }
        if (!this.PRELOADING) continue;
        if (title in this.resolved_titles) continue;
        this.resolved_titles[title] = 1;  //mark the title as "visited"
        var href = link.href;
        this.queue_resolving[href.split('?',1)] = href;
    }
    if (this.PRELOADING) {
        setTimeout(function() {DetikLangsung.preloading_job()}, this.preloading_delay);
    }
  },

  solve_remaining_links_cb: function (bind_onclick)  {
    for (var i=this.ulinks.length-1;i>=0; i--) {
        var link = this.ulinks[i];
        var title = link.textContent;
        var trimmed_title = this.trim(title);
        if (trimmed_title in this.cached_title_url) {
            link.href = this.cached_title_url[trimmed_title];
            link.title = this.signaturedl;
            link.removeEventListener("click", DetikLangsung.link_clicked, false);
            this.ulinks.splice(i,1);
        }
        else {
            //defer until user's click
            link.addEventListener("click", DetikLangsung.link_clicked, false);
        }
    }
  },
  
  link_clicked: function (e) {
    DetikLangsung.log("Link click meta:" + e.metaKey);
    DetikLangsung.solve(this.textContent, this.href, e.metaKey);
    e.stopPropagation();
    return false;
  },
  
  solve: function(title, href, meta_key) {
    var tab;
    //open empty page, just so that user has something to see while waiting
    if (meta_key) {
        tab = gBrowser.addTab("chrome://DetikLangsung/content/redirect.html");
        var tab_browser = gBrowser.getBrowserForTab(tab);
    }
    this.getHrefByTitleHref(title, href, function(href_r) {
        if (href == href_r) return;
        if (meta_key)
            gBrowser.getBrowserForTab(tab).loadURI(href_r);
        else
            gBrowser.loadURI(href_r);
    });
  },

  getHrefByTitleHref: function (title, href, callback) {
    var trimmed_title = this.trim(title);
    if (trimmed_title in this.cached_title_url) {
        callback(this.cached_title_url[trimmed_title]);
        return;
    }
    this.retrieve_portal_async(href, function() {
        callback(DetikLangsung.cached_title_url[trimmed_title] || href);
    });
  },

  retrieve_portal_async: function (href, callback) {
    this.log("Req:" + href);
    this.jobcounter++;
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return;
        DetikLangsung.jobcounter--;
        if (xhr.status != 200) return;
        DetikLangsung.parse_page(xhr.responseText, href); 
        DetikLangsung.log(href + " done");
        callback();
    };
    xhr.open("GET", href, true);
    xhr.send();
  },

  parse_page: function(body, page_href) {
    this.log("Parsing " + page_href);
    //use temporary div trick to parse DOM
    var tempDiv = this.doc.createElement('div');
    tempDiv.innerHTML = body;
    var anchors = tempDiv.getElementsByTagName("a");
    for (var i=0;i<anchors.length;i++) {
        var link = anchors[i];
        if (link.href.indexOf("/read/") == -1 && link.href.indexOf("/readfoto/") == -1) continue;
        //fix relative url, use anchor object to help me parse url
        if (link.protocol == "widget:") {
            var a = this.doc.createElement("a");
            a.href = page_href;
            link.protocol = a.protocol;
            link.hostname = a.hostname;
            link.port = a.port;
        }
        this.cached_title_url[this.trim(link.textContent)] = link.href;
    }
  },
  
  preloading_job: function () {
    this.log("Preloading job run");
    var refresh_link_if_alljobs_done = function() {
        if (DetikLangsung.jobcounter > 0) return;
        DetikLangsung.log("Refreshing links");
        DetikLangsung.solve_cache();
        DetikLangsung.solve_remaining_links_cb(false);
    };
    for (var key in this.queue_resolving)
        this.retrieve_portal_async(this.queue_resolving[key], refresh_link_if_alljobs_done);
    this.queue_resolving = {};   //clear it
  },
  
  //(trim17 http://yesudeep.wordpress.com/2009/07/31/even-faster-string-prototype-trim-implementation-in-javascript/
  trim: function (str){
    var len = str.length;
    if (len) {
        var whiteSpace = DetikLangsung.whiteSpace, i = 0;
        while (whiteSpace[str.charCodeAt(--len)]);
        if (++len)
            while (whiteSpace[str.charCodeAt(i)]){ ++i; }
        str = str.substring(i, len);
    }
    return str;
  },
  whiteSpace: []
};   

DetikLangsung.whiteSpace = [];
DetikLangsung.whiteSpace[0x0009] = true;
DetikLangsung.whiteSpace[0x000a] = true;
DetikLangsung.whiteSpace[0x000b] = true;
DetikLangsung.whiteSpace[0x000c] = true;
DetikLangsung.whiteSpace[0x000d] = true;
DetikLangsung.whiteSpace[0x0020] = true;
DetikLangsung.whiteSpace[0x0085] = true;
DetikLangsung.whiteSpace[0x00a0] = true;
DetikLangsung.whiteSpace[0x1680] = true;
DetikLangsung.whiteSpace[0x180e] = true;
DetikLangsung.whiteSpace[0x2000] = true;
DetikLangsung.whiteSpace[0x2001] = true;
DetikLangsung.whiteSpace[0x2002] = true;
DetikLangsung.whiteSpace[0x2003] = true;
DetikLangsung.whiteSpace[0x2004] = true;
DetikLangsung.whiteSpace[0x2005] = true;
DetikLangsung.whiteSpace[0x2006] = true;
DetikLangsung.whiteSpace[0x2007] = true;
DetikLangsung.whiteSpace[0x2008] = true;
DetikLangsung.whiteSpace[0x2009] = true;
DetikLangsung.whiteSpace[0x200a] = true;
DetikLangsung.whiteSpace[0x200b] = true;
DetikLangsung.whiteSpace[0x2028] = true;
DetikLangsung.whiteSpace[0x2029] = true;
DetikLangsung.whiteSpace[0x202f] = true;
DetikLangsung.whiteSpace[0x205f] = true;
DetikLangsung.whiteSpace[0x3000] = true;