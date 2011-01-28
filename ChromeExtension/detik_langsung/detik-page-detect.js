var DEBUG = false;
/*---browser specific functions---*/
function log (msg) {if (DEBUG) console.log(msg);}
function sendRequest(msg) {chrome.extension.sendRequest(msg);}
/*---end of browser specific functions---*/

var signaturedl = "Detik Langsung melangsungkan link ini!";
var p_su = /\.com\/(sepakbola)?\??[^\/]*$/;
var block1 = /(tv)|(suarapembaca)|\.detik\.com\/*$/;
var block2 = /\.com\/(infoanda)|(beritaterpopuler)|(video)|(indeks)\??[^\/]*$/;
var ulinks = [];

function link_clicked(e) {
    sendRequest({cmd:"SOLVE", title:this.innerText, href:this.href, meta_key:e.metaKey});
    if (e.metaKey)
        return false;
    return true;
}
function solve_remaining_links_cb(resp)  {
    for (var i=ulinks.length-1;i>=0; i--) {
        var link = ulinks[i];
        if (link.innerText in resp.titles) {
            link.href = resp.titles[link.innerText];
            link.title = signaturedl;
            link.onclick = undefined;
            log("Deleting " + link.innerText + " because backend found the href");
            delete ulinks[i];
        }
        else {
            //defer until user's click
            link.onclick = resp.bind_onlick? link_clicked : undefined;
        }
    }
}
function solve_remaining_links(bind_onclick) {
    log("Solving " + ulinks.length + " remaining links");
    var utitles = {};
    for (var key in ulinks) utitles[ulinks[key].innerText] = ulinks[key].href;
    sendRequest({cmd:"SOLVECACHE", utitles:utitles, bind_onclick:bind_onclick});
}

function init_extension() {
    log("Init at URL " + document.location.href);
    
    //first pass, collect all news links with "real" urls and short urls
    var real_link_title = {};
    var short_link = [];
    var anchors = document.getElementsByTagName("a");
    for (var i = 0; i < anchors.length; i++) {
        var link = anchors[i];
        if (link.innerText.length > 10 && link.href.search(p_su) == -1 ) {
            real_link_title[link.innerText] = link.href;
            continue;
        }
        if (link.innerText.length > 12 && link.host != 'twitter.com' && link.target != "_blank" && 
            link.href.search(p_su) > -1 && link.parentNode.className != "hnews" &&
            link.href.search(block1) == -1 && link.href.search(block2) == -1) { 
            short_link.push(link);
        }
    }

    //now iterate short links, try to solve it locally
    for (var i = 0; i < short_link.length; i++) {
        var link = short_link[i];
        if (link.innerText in real_link_title) {
            link.href = real_link_title[link.innerText];
            link.title = signaturedl; 
            continue;
        }
        ulinks.push(link);
    }
    delete real_link_title;
    //third pass, ask background for immediate resolving from available cache
    solve_remaining_links(true);
}

function handle_request(request) {
    if (!("cmd" in request)) return;
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