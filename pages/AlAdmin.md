# Introduction #

Al-Admin is a drop in php scripts and framework that provides instant administrative back-end/management console for any web site with MySQL. Allowing you to create [crud](http://en.wikipedia.org/wiki/Create,_read,_update_and_delete) forms for your tables rapidly. Used by actual sites such as [1](https://github.com/dodysw/dodysw-svn/tree/master/yayasankelola), [2](https://github.com/dodysw/dodysw-svn/tree/master/web_utils/mediamonitoring/), [3](https://github.com/dodysw/dodysw-svn/tree/master/ciscopip), [4](https://github.com/dodysw/dodysw-svn/tree/master/shopping/).

The intention of Al-Admin was similar to [Django Python](http://www.djangoproject.com)'s automatic admin module, although Al-Admin came alot earlier and at the time when ORM was not common yet.

# How it Works #

Developer first need to write a PHP class for each table to be administered, using existing sample code as guidance. This is quite similar in concept to an object relational modeling.

For each class, developer can add validation script, representation hint (e.g. view is as a pull-down list instead of radio buttons), and list of tables to display in the administration view.

# Screen Shots #

![http://i.imgur.com/HM1AR.png](http://i.imgur.com/HM1AR.png)

Al-Admin home page

![http://i.imgur.com/9Bln9.png](http://i.imgur.com/9Bln9.png)

UI of automatically generated standard CRUD grid

![http://i.imgur.com/pSxlp.png](http://i.imgur.com/pSxlp.png)

Supports detail/child tables, and even the user manager is built the same way

![http://i.imgur.com/xerKw.png](http://i.imgur.com/xerKw.png)

All tables are instantly provided with editable forms

![http://i.imgur.com/IgNoM.png](http://i.imgur.com/IgNoM.png)

And automatically generated one table row view

![http://i.imgur.com/B2eHn.png](http://i.imgur.com/B2eHn.png)

Search functionalities built-in to all tables, with selectable field scope

# Source Code #

[Al-Admin source code](https://github.com/dodysw/dodysw-svn/tree/master/web_utils/aladmin) is available. Warning, it has not been updated since 2005.
