<?php
/*
Project MDG - quiz game ranking generated from MDG subset of world development indicator
Copyright 2011 - Dody Suria Wijaya <dodysw@gmail.com>
License is GPL v3.

Description: 
QuizTypes generate a question, an array of possible choices string, and answer string. 
Quiz randomly pick one QuizTypes, question id, and return as response.
Answer expect hash and answer string, and check the hash. If correct, remove hash from session so that it's not used anymore. It return bool of correctness.
*/

$secret_key = "THISISMYSECRET";

function quiz_1() {
    /*
    "Which of the following countries has the [highest|lowest] [series] between 1990 and 2008"
    */
    include "config.inc.php";
    
    $link = mysql_connect($DB_HOST, $DB_USER, $DB_PASS) or die("Unable to connect:".mysql_error());
    mysql_select_db($DB_NAME) or die("Could not select database:".mysql_error());
    
    //it's possible that this indicator has no data. repeat until there is data
    $country_name = "";
    while ($country_name == "") {
        $sql = "select `series code`, `series name` from MDG_Series order by rand() limit 1";
        $result = mysql_query($sql) or die('Query failed: ' . mysql_error());
        list($series_code, $series_name) = mysql_fetch_row($result);
        
        $has_highest = rand(0,1);
        $sql = sprintf("select a.`country code`, `country name` from MDG_Data_y a left join MDG_Country b on a.`country code`= b.`country code` and b.region != 'Aggregates' where `series code`='%s' and value = (select ".($has_highest? "max": "min")."(value) from MDG_Data_y a inner join MDG_Country b on a.`country code`= b.`country code` and b.region != 'Aggregates' where `series code`='%s' and value > 0) group by `country code`",
            mysql_real_escape_string($series_code),
            mysql_real_escape_string($series_code)
            );
        $result = mysql_query($sql) or die('Query failed: ' . mysql_error());
        list($country_code, $country_name) = mysql_fetch_row($result);
    }
    $options = array($country_name);
    
    //fake answers
    $sql = sprintf("select `country name` from MDG_Country where `country code` != '%s' and region != 'Aggregates' order by rand() limit 3",
        $country_code);
    $result = mysql_query($sql) or die('Query failed: ' . mysql_error());
    while($row = mysql_fetch_row($result)) {
        $options[] = $row[0];
    }
    
    
    shuffle($options);
    $question = sprintf("Which of the following countries has the %s %s between 1990 and 2008",
        $has_highest? "highest": "lowest",
        $series_name);
    
    return array(
        "question" => $question,
        "options" => $options,
        "answer" => $country_name
        );
}

function quiz_2() {
    /*
    Which of the following number is nearest to [series] of [country] at year [year]
    */
    include "config.inc.php";
    
    $link = mysql_connect($DB_HOST, $DB_USER, $DB_PASS) or die("Unable to connect:".mysql_error());
    mysql_select_db($DB_NAME) or die("Could not select database:".mysql_error());

    //it's possible that this indicator has no data. repeat until there is data
    $rows = array();
    while (count($rows) < 4) {
        $sql = "select `series code`, `series name` from MDG_Series order by rand() limit 1";
        $result = mysql_query($sql) or die('Query failed: ' . mysql_error());
        list($series_code, $series_name) = mysql_fetch_row($result);
        
        $year = rand(1990,2008);
        $sql = sprintf("select a.`country code`, a.`value`, `country name` from MDG_Data_y a left join MDG_Country b on a.`country code`= b.`country code` where `series code`='%s' and value > 0 and a.year = '%d'order by rand() limit 4",        
            mysql_real_escape_string($series_code),
            mysql_real_escape_string($year)
            );
        $result = mysql_query($sql) or die('Query failed: ' . mysql_error());
        $rows = array();
        while($row = mysql_fetch_assoc($result)) {
            $rows[] = $row;
        }
    }    
    $answer = number_format($rows[0]["value"], 2);
    $country_name = $rows[0]["country name"];
    $options = array();
    foreach ($rows as $row) {
        $options[] = number_format($row["value"], 2);
    }
    shuffle($options);


    $question = sprintf("Below is %s in %d. Which one belongs to %s?",
        $series_name,
        $year,
        $country_name);

    return array(
        "question" => $question,
        "options" => $options,
        "answer" => $answer
        );

}


function quiz_3() {
    /*
    Which [goal|target] does [indicator] related to
    */
    include "config.inc.php";
    
    $link = mysql_connect($DB_HOST, $DB_USER, $DB_PASS) or die("Unable to connect:".mysql_error());
    mysql_select_db($DB_NAME) or die("Could not select database:".mysql_error());

    $sql = "select `series code`, `Goal`, `Target`, `series name` from MDG_Series order by rand() limit 1";
    $result = mysql_query($sql) or die('Query failed: ' . mysql_error());
    list($series_code, $goal, $target, $series_name) = mysql_fetch_row($result);
    
    $options = array();

    $is_goal = rand(0,1);
    if ($is_goal) {
        $sql = sprintf("select `Goal` from MDG_Series where `goal` != '%s' group by goal order by rand() limit 3",
            mysql_real_escape_string($goal));
    }
    else {
        $sql = sprintf("select `Target`  from MDG_Series where `target` != '%s' group by target order by rand() limit 3",
            mysql_real_escape_string($target));
    }
    $result = mysql_query($sql) or die('Query failed: ' . mysql_error());
    while ($row = mysql_fetch_row($result)) {
        $options[] = $row[0];
    }
    $options[] = $is_goal? $goal: $target;
    sort($options);
    
    $answer = $is_goal? $goal: $target;    
    $question = sprintf("Which millennium development %s does %s relate to?",
        $is_goal? "goal": "target",
        $series_name);
    
    return array(
        "question" => $question,
        "options" => $options,
        "answer" => $answer
        );


}

function quiz_4() {
    /*
    The following countries are categorized as [income group]. Select one country that is NOT in this income group.
    */
    include "config.inc.php";
    
    $link = mysql_connect($DB_HOST, $DB_USER, $DB_PASS) or die("Unable to connect:".mysql_error());
    mysql_select_db($DB_NAME) or die("Could not select database:".mysql_error());

    $sql = "select `Income Group` from MDG_Country where `Income Group` != 'Aggregates' group by `Income Group` order by rand() limit 2";
    $result = mysql_query($sql) or die('Query failed: ' . mysql_error());
    $income_groups = array();
    while ($row = mysql_fetch_row($result)) {
        $income_groups[] = $row[0];
    }

    $options = array();
    $sql = sprintf("select `country name` from MDG_Country where `Income Group`='%s' order by rand() limit 3",
        mysql_real_escape_string($income_groups[0]));
    $result = mysql_query($sql) or die('Query failed: ' . mysql_error());
    while ($row = mysql_fetch_row($result)) {
        $options[] = $row[0];
    }
    $sql = sprintf("select `country name` from MDG_Country where `Income Group`='%s' order by rand() limit 1",
        mysql_real_escape_string($income_groups[1]));
    $result = mysql_query($sql) or die('Query failed: ' . mysql_error());
    while ($row = mysql_fetch_row($result)) {
        $options[] = $row[0];
    }
    $answer = $options[3];

    shuffle($options);
    
    $question = sprintf("The following countries are categorized as %s. Select one country that is NOT in this income group.",
        $income_groups[0]);
    
    return array(
        "question" => $question,
        "options" => $options,
        "answer" => $answer
        );
}

function GET_quiz($params) {
    /* decide a question, return as json
    */
    global $secret_key;

    //decide from set of question types
    $quiz_type = rand(1,4);
    $payload = call_user_func("quiz_".$quiz_type);
    
    //hash the answer so that only us can check the correctness
    $uniqid = uniqid();
    $quiz_id = md5($secret_key.$uniqid);
    $payload["hash"] = $uniqid."-".$quiz_id;
    
    session_start();
    $_SESSION[$quiz_id] = $payload["answer"];
    unset($payload["answer"]);
    
    //return json consisting of: question string, id/hash, choices
    return json_encode($payload);
}

function GET_ranking($params) {
    $payload = array();
    
    include "config.inc.php";            
    $link = mysql_connect($DB_HOST, $DB_USER, $DB_PASS) or die("Unable to connect:".mysql_error());
    mysql_select_db($DB_NAME) or die("Could not select database:".mysql_error());
    $sql = sprintf("select username, country, score, datediff(curdate(), last_activity) last_activity from Score order by score desc");
    $result = mysql_query($sql) or die('Query failed: ' . mysql_error());
    $payload["ranks"] = array();
    while ($row = mysql_fetch_assoc($result)) {
        $payload["ranks"][] = $row;
    }
    $payload["status"] = "ok";
    return json_encode($payload);
}

function POST_answer($params) {
    /* accept a quiz's answer, 
    */
    global $secret_key;
    $hash = $params["hash"];
    $answer = $params["answer"];
    $payload = array();
    $temp = explode("-", $hash);
    $uniqid = $temp[0];
    $quiz_id = $temp[1];
    $hash_compare = md5($secret_key.$uniqid);
    if ($hash_compare != $quiz_id) {
        $payload["status"] = "hash error";
        return json_encode($payload);
    }
    
    session_start();
    if (!isset($_SESSION["score"]))
        $_SESSION["score"] = 0;

    if (isset($_SESSION[$quiz_id])) {
        $payload["status"] = "ok";
        $payload["is_correct"] = ($_SESSION[$quiz_id] == $answer);
        $payload["answer"] = $_SESSION[$quiz_id];
        unset($_SESSION[$quiz_id]);
        
        //update user's score
        if (isset($_SESSION["username"])) {
            include "config.inc.php";            
            $link = mysql_connect($DB_HOST, $DB_USER, $DB_PASS) or die("Unable to connect:".mysql_error());
            mysql_select_db($DB_NAME) or die("Could not select database:".mysql_error());
            $sql = sprintf("insert Score (username, country, score) values ('%s', '%s', 1) on duplicate key update score=score+(%d), tries=tries+1",
                mysql_real_escape_string($_SESSION["username"]),
                mysql_real_escape_string(isset($_SESSION["country"])? $_SESSION["country"]: ""),
                $payload["is_correct"]? 1: -1
                );
            $result = mysql_query($sql) or die('Query failed: ' . mysql_error());
            
            $_SESSION["score"] += $payload["is_correct"]? 1: -1;
        }
    }
    else {
        $payload["status"] = "expired";
    }
    $payload["score"] = $_SESSION["score"];
    return json_encode($payload);
}

function GET_userprofile($params) {
    session_start();
    $payload = array();
    if (!isset($_SESSION["username"])) {
        $payload["logged_in"] = false;
    }
    else {    
        include "config.inc.php";
        $link = mysql_connect($DB_HOST, $DB_USER, $DB_PASS) or die("Unable to connect:".mysql_error());
        mysql_select_db($DB_NAME) or die("Could not select database:".mysql_error());
        $sql = sprintf("select country, score, last_activity from Score where username='%s'",
                    mysql_real_escape_string($_SESSION["username"]));
        $result = mysql_query($sql) or die('Query failed: ' . mysql_error());
        $row = mysql_fetch_array($result);
        
        $_SESSION["score"] = intval($row["score"]);
        $_SESSION["country"] = $row["country"];
        
        $payload["logged_in"] = true;
        $payload["username"] = $_SESSION["username"];
        $payload["country"] = $row["country"];
        $payload["score"] = $_SESSION["score"];
        $payload["last_activity"] = $row["last_activity"];
    }
    return json_encode($payload);
}

function POST_login($params) {
    require 'lightopenid/openid.php';
    try {
        $openid = new LightOpenID;
        if(!$openid->mode) {
            $openid->identity = $params["openid_provider"];
//             $openid->identity = 'https://www.google.com/accounts/o8/id';
//             $openid->identity = 'http://yahoo.com/';
            $openid->required = array('contact/email');
            if (!isset($params["return_url"])) {
                return json_encode(array("status"=>"error", "error_message"=>"need return url"));
            }
            session_start();
            $_SESSION["openid_final_return_url"] = $params["return_url"];
            $ch = curl_init('http://api.hostip.info/country.php?ip='.$_SERVER['REMOTE_ADDR']);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
            $_SESSION["country"] = curl_exec($ch);
            return json_encode(array("status"=>"ok","logged_in"=>false, "redirect_to"=>$openid->authUrl(), "country"=>$_SESSION["country"]));
        }
    } catch(ErrorException $e) {
        return json_encode(array("status"=>"error", "error_message"=>$e->getMessage()));
    }
}

function GET_login($params) {
    require 'lightopenid/openid.php';
    try {
        session_start();
        $openid = new LightOpenID;
        if($openid->mode == 'cancel') {
            header("Location:".$_SESSION["openid_final_return_url"]);
            return;
        } 
        else {
            //this should be enabled if hosting support https protocol on curl
//             if ($openid->validate()) {
                $attr = $openid->getAttributes();
                $_SESSION["username"] = $attr["contact/email"];

                include "config.inc.php";            
                $link = mysql_connect($DB_HOST, $DB_USER, $DB_PASS) or die("Unable to connect:".mysql_error());
                mysql_select_db($DB_NAME) or die("Could not select database:".mysql_error());
                $sql = sprintf("insert Score (username, country, score) values ('%s', '%s', %d) on duplicate key update country='%s'",
                    mysql_real_escape_string($_SESSION["username"]),
                    mysql_real_escape_string($_SESSION["country"]),
                    mysql_real_escape_string($_SESSION["score"]),
                    mysql_real_escape_string($_SESSION["country"])
                    );
                $result = mysql_query($sql) or die('Query failed: ' . mysql_error());
                header("Location:".$_SESSION["openid_final_return_url"]);
                return;
//             }
//             else {
//                 return json_encode(array("status"=>"ok", "logged_in"=>false, "result"=>"not logged in"));
//             }
        }
    } catch(ErrorException $e) {
        return json_encode(array("status"=>"error", "error_message"=>$e->getMessage()));
    }
}

function POST_logout($params) {
    session_start();
    session_destroy();
}


?>