// ==UserScript==
// @include http://us.detik.com/*
// @include http://www.detik.com/*
// ==/UserScript==
var pattern = /\.com\/(sepakbola)?\??[^\/]*$/;
var skipped_count;

function popUp(vis, msg) {
    var tbody = document.getElementsByTagName("body")[0];
    var popup = document.getElementById('darkenScreenObjectPopup');
    var opacity = "80";var opaque = (opacity / 100);
    if (!popup) {
        var popnode = document.createElement('div');
            popnode.style.position = 'fixed';
            popnode.style.bottom = "1px";
            popnode.style.left = "2px";
            popnode.style.padding = "0px";
            popnode.style.paddingLeft = "10px";
            popnode.style.paddingRight = "10px";
            popnode.style.backgroundColor = "yellow";
            popnode.style.opacity = opaque;
            popnode.style.MozOpacity = opaque;
            popnode.style.zIndex = "60";
            popnode.style.borderStyle = "dashed";
            popnode.style.display = 'none';
            popnode.id = 'darkenScreenObjectPopup';
            popnode.innerHTML = msg;
        tbody.appendChild(popnode);
        popup = document.getElementById('darkenScreenObjectPopup');  // Get the object.
    }
    popup.style.display = vis? 'block': 'none';
}


function link_clicked(e) {
    //on some occation, real links is supplied at the same page on different part, let's check that first
    var found_href = false;
    var anchors = document.getElementsByTagName("a");
    for (var i = 0; i < anchors.length; i++) {
        var el = anchors[i];
        if (el.innerText.indexOf(this.innerText) ==  -1 || el.href.search(pattern) > -1) continue;
        found_href = el.href;
        break;
    }
    
    opera.postError("Clicked: " + this.innerText);
    popUp(true, '<span style="color:red;font:13px verdana;"><b>DETIK LANGSUNG</b></span> <span style="color:green;font:13px verdana">Telah membantu <b>' + skipped_count + '</b> kali</span>');

    if (found_href) {
        opera.postError("Direct found!");
        opera.extension.postMessage(JSON.stringify({cmd:"INCSKIP"}));
        window.stop();
        window.location.href = found_href;
    }
    else {
        //ask bg process to look forward on channel portal page
        opera.extension.postMessage(JSON.stringify({cmd:"SOLVE", title:this.innerText, href:this.href}));
    }    
    return false;
}

opera.extension.onmessage = function(event){
    opera.postError("background process sent: " + event.data);
    var respose = JSON.parse(event.data);
    if (respose.cmd == "COUNT") {
        skipped_count = respose.skipped_count;
    }
    else if (respose.cmd == "REDIRECT") {
        window.stop();
        window.location.href = respose.href;
    }
};

function init_extension() {
    for (var i = 0; i < document.links.length; i++) {
        var link = document.links[i];
        if (link.innerText.length <= 2 || link.target == "_blank" || link.href.search(pattern) == -1 || link.parentNode.className == "hnews")
            continue;
        link.onclick = link_clicked;
    }
    opera.postError("Injected script initialized");
}

window.addEventListener("DOMContentLoaded", init_extension, false);
opera.extension.postMessage(JSON.stringify({cmd:"INIT"}));