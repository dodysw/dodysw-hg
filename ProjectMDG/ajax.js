var username;
var score;
var country;

var api_server = "http://mdg.comlu.com/";

//stupid IE not following standard...
function addListener ( eventName, control, handler) {
    //Check if control is a string
    // https://developer.mozilla.org/en/Core_JavaScript_1.5_Reference/Operators/Comparison_Operators
    if (control === String(control))
        control = document.getElementById(control);
    if (control.addEventListener) { //Standard W3C
        return control.addEventListener(eventName, handler, true);
    } else if (control.attachEvent) { //IExplore
        return control.attachEvent("on"+eventName, handler);
    } else {
        return false;
    }
}

function request(method, url, params, ready_func) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = ready_func;
    xhr.open(method,url,ready_func != undefined);
    if (method == "POST") {
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    }
    xhr.send(params);
    return xhr.responseText;
}

function get_nextset_question() {
    var resp = request("GET", api_server+"api.php?do=quiz");
    if (resp) {
        resp = JSON.parse(resp);
        document.getElementById("question").innerHTML = resp["question"];
    }
    var hash = resp["hash"];
    var form = document.forms[0];
    
    while (form.childNodes.length >= 1 ) {
        form.removeChild(form.firstChild );
    }
    
    var answer;
    var answered = false;
    for (var i = 0; i < resp["options"].length; i++) {
        var new_input = document.createElement("input");
        new_input.name = "answer";
        new_input.value = resp["options"][i];
        new_input.id = resp["options"][i];
        new_input.type = "radio";
        new_input.onclick = function() {
            if (answered) return;
            answer = this.id;
            document.getElementById("bt_answer").disabled = "";
        }
        form.appendChild(new_input);
        
        var new_input = document.createElement("label");
        new_input.htmlFor = resp["options"][i];
        new_input.innerHTML = resp["options"][i];
        new_input.id = resp["options"][i]+"_label";
        form.appendChild(new_input);
        
        var new_input = document.createElement("br");
        form.appendChild(new_input);
    }
    
    var new_input = document.createElement("br");
    form.appendChild(new_input);
    var new_input = document.createElement("input");
    new_input.type = "button";
    new_input.id = "bt_answer";
    new_input.value = "answer";
    new_input.disabled = "disabled";
    form.appendChild(new_input);
    new_input.onclick = function() {
        if (answered) {
            get_nextset_question();
            return;
        }
        answered = true;
        var params = "hash="+encodeURIComponent(hash)+"&answer="+encodeURIComponent(answer);
        var resp = request("POST", api_server+"api.php?do=answer", params);
        if (resp) {
            resp = JSON.parse(resp);
            if (resp["status"] == "ok") {
                if (resp["is_correct"]) {
                    this.value = "Correct! Click for next quiz";
                }
                else {
                    this.value = "Incorrect. The correct answer is " + resp["answer"] + ". Click for next quiz.";
                    document.getElementById(resp["answer"]+"_label").style.borderStyle = "solid";
                }
            }
            else {
                this.value = "Question has expired. Click for next quiz.";
            }
            score = resp["score"];
        }
        update_login_text();
    }
}

function sign_in($provider) {
    document.getElementById("login").innerHTML = "Logging in...";
    var url = api_server+"api.php?do=login";
    request("POST", url, "return_url=" + encodeURIComponent(window.location.href)+"&openid_provider=" + encodeURIComponent($provider), function () {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText) {
                var resp = JSON.parse(this.responseText);
                if (resp["redirect_to"] != undefined) {
                    window.location = resp["redirect_to"];
                    return false;
                }
                else if (resp["logged_in"]) {
                    username = resp["username"];
                    fetch_profile();
                }
            }        
        }
    });
    return false;
}

function sign_out() {
    request("POST", api_server+"api.php?do=logout", null, function() {});
    username = null;
    score = null
    update_login_text();
    return false;
}

function fetch_profile() {
    var resp = request("GET", api_server+"api.php?do=userprofile");
    if (resp) {
        resp = JSON.parse(resp);
        if (resp["logged_in"]) {
            username = resp["username"];
            score = resp["score"];
            country = resp["country"];
        }
    }
    update_login_text()
}

function update_login_text() {
    if (username) {
        var flag_img = "";
        if (country) {
            flag_img = '<img src="flag/' + country.toLowerCase() + '.png">';
        }
        document.getElementById("login").innerHTML = '<a href="ranking.html?#' + username + '">' + username +'</a> '+ flag_img +' (' + score + '). <a href="" onclick="return sign_out();">Logout</a>';
    }
    else {
        document.getElementById("login").innerHTML = '<a href="" onclick="return sign_in(\'http://www.google.com/accounts/o8/id\');">Sign in with Google</a> or <a href="" onclick="return sign_in(\'http://www.yahoo.com\');">Yahoo</a> to place yourself in <a href="ranking.html">ranking</a>.';                        
    }
}