var DEBUG = false;
/*---browser specific functions---*/
function log (msg) {if (DEBUG) console.log(msg);}
function sendRequest(msg) {chrome.extension.sendRequest(msg);}
/*---end of browser specific functions---*/

var signaturedl = "Detik Langsung melangsungkan link ini!";
var p_su = /\.com\/(sepakbola)?\??[^\/]*$/;
var block1 = /(tv|suarapembaca)\.detik\.com\/.*$/;
var block2 = /\.com\/(infoanda|beritaterpopuler|video|indeks)\??[^\/]*$/;
var ulinks = [];
var anchors;

function link_clicked(e) {
    sendRequest({cmd:"SOLVE", title:this.textContent, href:this.href, meta_key:e.metaKey});
    if (!e.metaKey)
        this.textContent = "Tunggu ya, detik langsung mikir dulu...";
    e.stopPropagation();
    return false;
}
function solve_remaining_links_cb(resp)  {
    for (var i=ulinks.length-1;i>=0; i--) {
        var link = anchors[ulinks[i]];
        if (link.textContent in resp.titles) {
            link.href = resp.titles[link.textContent];
            link.title = signaturedl;
            link.onclick = undefined;
            log("Deleting " + link.textContent + " because backend found the href");
            delete ulinks[i];
        }
        else {
            //defer until user's click
            link.onclick = resp.bind_onclick? link_clicked : undefined;
        }
    }
}
function solve_remaining_links(bind_onclick) {
    log("Solving " + ulinks.length + " remaining links");
    var utitles = {};
    for (var key in ulinks) utitles[anchors[ulinks[key]].textContent] = anchors[ulinks[key]].href;
    sendRequest({cmd:"SOLVECACHE", utitles:utitles, bind_onclick:bind_onclick});
}

function init_extension() {
    log("Init at URL " + document.location.href);
    anchors = document.getElementsByTagName("a");
    
    //first pass, collect all news links with "real" urls and short urls
    var real_link_title = {};
    var short_link = [];
    for (var i = 0; i < anchors.length; i++) {
        var link = anchors[i];
        if (link.textContent.length > 10 && link.href.search(p_su) == -1 ) {
            real_link_title[link.textContent] = link.href;
            continue;
        }
        if (link.textContent.length > 12 && link.host != 'twitter.com' && link.target != "_blank" && 
            link.href.search(p_su) > -1 && link.parentNode.className != "hnews" &&
            link.href.search(block1) == -1 && link.href.search(block2) == -1) { 
            short_link.push(i);
        }
    }

    //now iterate short links, try to solve it locally
    for (var i = 0; i < short_link.length; i++) {
        var link = anchors[short_link[i]];
        if (link.textContent in real_link_title) {
            link.href = real_link_title[link.textContent];
            link.title = signaturedl; 
            continue;
        }
        ulinks.push(short_link[i]);
    }
    real_link_title = null;
    short_link = null;
    //third pass, ask background for immediate resolving from available cache
    solve_remaining_links(true);
}

function handle_request(request) {
    if (!("cmd" in request)) return;
    log("IS Received: " + request.cmd);
    switch (request.cmd) {
        case "REDIRECT":
            window.location.href = request.href;
            break;
        case "RSOLVECACHE":
            solve_remaining_links_cb(request);
            break;
        case "REFRESHLINK":
            log("Content script received message");
            solve_remaining_links(false);
            break;
    }
}

chrome.extension.onRequest.addListener(function(request, sender, senderResponse) { handle_request(request);senderResponse(null);});
init_extension();