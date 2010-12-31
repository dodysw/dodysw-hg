var pattern = /\.com\/(sepakbola)?\??[^\/]*$/;
var skipped_count;

function popUp(vis, msg) {
    var tbody = document.getElementsByTagName("body")[0];
    var popup = document.getElementById('darkenScreenObjectPopup');
    var opacity = "80";var opaque = (opacity / 100);
    if (!popup) {
        var popnode = document.createElement('div');
            popnode.style.position = 'fixed';
            popnode.style.bottom = "20px";
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
    //on some occasion, real links is supplied at the same page on different part, let's check that first
    var found_href = false;
    var anchors = document.getElementsByTagName("a");
    for (var i = 0; i < anchors.length; i++) {
        var el = anchors[i];
        if (el.innerText.indexOf(this.innerText) ==  -1 || el.href.search(pattern) > -1) continue;
        found_href = el.href;
        break;
    }
    
    console.log("Clicked: " + this.innerText);
    popUp(true, '<span style="color:red;font:13px verdana;"><b>DETIK LANGSUNG</b></span> <span style="color:green;font:13px verdana">Telah membantu <b>' + skipped_count + '</b> kali</span>');

    if (found_href) {
        console.log("Direct found!");
        chrome.extension.sendRequest({cmd:"INCSKIP"});
        window.stop();
        window.location.href = found_href;
    }
    else {
        //ask bg process to look forward on channel portal page
        chrome.extension.sendRequest({cmd:"SOLVE", title:this.innerText, href:this.href}, function (response) {
            window.stop();
            window.location.href = response.href;
        });
    }    
    return false;
}

function init_extension() {
    for (var i = 0; i < document.links.length; i++) {
        var link = document.links[i];
        if (link.target == "_blank" || link.href.search(pattern) == -1 || link.parentNode.className == "hnews")
            continue;
        link.onclick = link_clicked;
    }
}

init_extension();
chrome.extension.sendRequest({cmd:"INIT"}, function (response) {
    skipped_count = response.skipped_count;
});