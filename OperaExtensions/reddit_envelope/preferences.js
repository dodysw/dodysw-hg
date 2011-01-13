var minimum_update_freq = 60000;
var ms_to_minute_ratio = 60000
var option_page = document.URL.substring(document.URL.lastIndexOf('/')+1) == "options.html";
window.addEventListener("load", function(){
    var el = document.forms[0].elements;
    if (widget.preferences["username"])
        el["username"].value = widget.preferences["username"];
    if (widget.preferences["passwd"])
        el["passwd"].value = widget.preferences["passwd"];
    
    if (option_page) {
        document.getElementById("title").innerText = window.widget.name;
        document.getElementById("version").innerText = "version " + window.widget.version;
        document.getElementById("author").innerHTML = "<a href='" + window.widget.authorHref + "'>By " + window.widget.author + "</a>";
        if (widget.preferences["update_freq"])
            el["update_freq"].value = parseInt(parseInt(widget.preferences["update_freq"]) / ms_to_minute_ratio);

        if (widget.preferences["click_icon_for"] == "inbox")
            el["click_icon_for_inbox"].checked = true;
        else if (widget.preferences["click_icon_for"] == "update")
            el["click_icon_for_update"].checked = true;
        else {
            el["click_icon_for_inbox"].checked = true;
        }
    }
    
    document.forms[0].addEventListener("submit", function() {
        var el = document.forms[0].elements;
        widget.preferences["username"] = el["username"].value;
        widget.preferences["passwd"] = el["passwd"].value;
        if (option_page) {
            if (!el["update_freq"].value)
                el["update_freq"].value = minimum_update_freq;
            widget.preferences["update_freq"] = parseInt(el["update_freq"].value) * ms_to_minute_ratio;
            if (widget.preferences["update_freq"] < minimum_update_freq)
                widget.preferences["update_freq"] = minimum_update_freq;
                
            widget.preferences["click_icon_for"] = el["click_icon_for_inbox"].checked? "inbox": "update";
        }
        opera.extension.postMessage("LOGIN");
        window.close();
    }, false);
    
}, false);
