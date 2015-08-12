# Introduction #

The project displays key performance Indicators (KPI) of an oil company using regular large LCD TV hanged on office areas connected to existing network computing headless CPU via standard TV Tuner. Each CPU would open a designated web sites depending on their location. Basically this is the limit of the hardware requirement, as long as it has a web browser, then it can be used for digital signage.

# Software Architecture #

The website was written in regular ASP.NET/C# with client-side JavaScripts to trigger an automated URL changes based on predefined list of URLS to visit, thus simulating a slide show. Slide admin edits the list to adjust the slide shows' orders, or add, edit, delete URLs to design the information presented in slide show.

The reason for this design is for maximum flexibility and separation of concern and tasks. Simple static information can be written by end users using plain HTML or in a SharePoint site. More advanced slides can be written by programmers, including dynamic queries to back-end transactional database, chart generation, and business reports.

The slide software was written in less than a week, and most of the efforts went to creating KPI slides that queries database and either present as tabular data with traffic-light style indicators, or chart using [dotNetCharting](http://www.dotnetcharting.com/).

# In Action #

![http://i.imgur.com/aH8Hnl.jpg](http://i.imgur.com/aH8Hnl.jpg)

Digital signage early development trial located on lobby area

![http://i.imgur.com/N7qgZl.jpg](http://i.imgur.com/N7qgZl.jpg)

One of my colleague proudly pose in front of a slide showing a production performance chart

<sup>Thanks to Angela Syeni for providing me with the photo</sup>