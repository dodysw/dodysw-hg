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
include 'apilib.php';
header('Content-type: application/json');
echo call_user_func($_SERVER['REQUEST_METHOD']."_".$_REQUEST["do"], $_REQUEST);

?>