Project MDG is a web app I wrote for The World Bank Apps for Development competition.

## Design ##

The app is composed of back-end side with RESTful API and clients. The back end handles all data interfacing to MDG dataset, generate question set, check answers, OpenID authentication, user session, and score and ranking tracking. It was developed with PHP and MySQL. The code is very readable as it uses no web frameworks and only require [lightopenid library](http://code.google.com/p/lightopenid/) for its openid authentication and ip-to-country service by [hostip.info](http://hostip.info).

The clients provides UI and interface with back-end purely from its RESTful API. As a proof of concept of their separation of concern, one client has been developed that is entirely browser-based (html file with javascript).

## Try It ##

One instance has been prepared on [mdg.comlu.com](http://mdg.comlu.com/client.html). You can play with it and share your score with everyone in the world.

## Source Code ##

You can view all [source codes](http://code.google.com/p/dodysw-hg/source/browse/ProjectMDG/) of this apps.

[![](http://appsfordevelopment.s3.amazonaws.com/AppsForDev_291x56.gif)](http://appsfordevelopment.challengepost.com/)