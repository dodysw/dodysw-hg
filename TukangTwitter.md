# Introduction #

Tukang Twitter is a set of twitter clients wrote for seven mobile platforms that allows user to twit message to a single predefined twitter account, and view the feeds. Its only purpose is to teach me the practicality of programming on each popular mobile platforms.

The base line is a twitter posting site I previously made, build on Django Python deployed to GAE, it took about 45 minutes to write.

Note, after this application was written in early 2010, [Twitter has been enforcing OAuth](http://dev.twitter.com/pages/oauth_faq) for its API usage, which means the app will likely stop working and has to be modified. However the gist of this review should still applies.

**Update March 2011:** Added windows mobile 7, and Mac version that works with twitter new authentication.

# Mac #

This is not mobile platform, but the [Mac App Store](http://www.apple.com/mac/app-store/) popularized the platform by appealing to iPhone apps creators, so it's very much relevant to quickly look how easy it is for iPhone developers to jump into desktop app creation.

  * IDE: XCode 3.2.5, Mac OS X 10.6 SDK
  * Language: Objective-C 2.0, Cocoa
  * Twitter lib: MGTwitterEngine, OAuthConsumer, TouchJSON
  * Development platform: Mac OS X only
  * Shares a (unsurprisingly) similar development experience with iPhone, equals in all respect for all NS classes, with a bit of learning curve relearning the equivalent of UI classes from UIKit to Cocoa. E.g., UITableView to  NSTableView.
  * Workflow similar to iPhone: start creating outlets and xib, drag arrow to delegate classes, define the delegation methods, and so on. Documentations are clear and top notch, but can be a lengthy reading. Trying demo app (usually referred to on each class documentation) is recommended to TLDR;.
  * MGTwitterEngine seemed to be unmaintained, and left in a uncompileable state with messy dependencies, after hours stumbled into [a twitter client tutorial that faced the same issue and actually solved it](http://brandontreb.com/creating-a-twitter-client-for-osx-part-1/). I promised not to look at the part-2 of the article to keep my "research" objective.
  * Understanding MGTwitterEngine asynchronous+delegation and its connectionId can be tricky as the class is literally undocumented
  * A sense of less demand for code performance; knowing it will be running on full powered desktop; but being used to mobile development surely is beneficial to create memory thrift and speedy apps.

![http://i.imgur.com/0Ry6H.png](http://i.imgur.com/0Ry6H.png)

Total development time 3 hours and 25 minutes, half of it for compiling MGTwitterEngine, and some issue with active target not pointing to the right .pch file (error when adding .c files), about an hour of studying the desktop Cocoa classes.

# Windows Mobile 7 #

  * IDE: Visual Studio 2010 Express for Windows Phone
  * Language: C#, .NET 3.5 Compact, Silverlight
  * Twitter lib: [TweetSharp](http://tweetsharp.codeplex.com/) v2
  * Development platform: Windows 7 only, must not be virtualized
  * Great IDE, probably the best, layout designer is good but the outer gray ribbon gets in the way visually, regularly need to zoom in, love the default left-right designer-xaml code format.
  * Very fast emulator
  * Coming from C# programmer, and previous experience doing it for Windows Mobile 6, it's been pretty much zero learning, with few minutes of familiarizing the Dispatcher.BeginInvoke idiom for code that interact with UI, which is specific to WP7
  * The inability to run vs2010 Windows Phone on VM forced me to look for windows machine
  * Takes a while to understand how tweetsharp run on Twitter's OAuth implementation, the sample code in the documentation does not help a lot, but quickly found that we can get around the OAuth authorization process by specifying token and token secret since this apps only tweet to its own account

![http://i.imgur.com/Qh9rNl.png](http://i.imgur.com/Qh9rNl.png)

![http://i.imgur.com/EpOXal.png](http://i.imgur.com/EpOXal.png)

Total development time: 1 hour 3 minutes, mostly because I have done this before on Windows Mobile 6, but should be faster by 30 minutes if not caused by twitter's OAuth.

**Update April 2011:** Finally tried on real device, LG-C900, a lend from Best Buy Mobile. Device need to be linked to a Windows Live account with App Hub developer account via a simple registration process (and installing Zune). No need for complex certification and signing (or at least I can just press run on visual studio and it simply...run).

# iPhone #

  * IDE: XCode, iPhoneOS SDK 3.1
  * Language: Objective-C
  * Twitter lib: [MGTwitterEngine](https://github.com/mattgemmell/MGTwitterEngine)
  * Development platform: Mac only
  * Note: unrobust, wrote as fast as I could to fulfill given requirement
  * Great contextual code documentation available
  * Very fast simulator, maybe faster than the original device
  * Even coming from C developer Objective-C syntax is stupendously awkward at first, however I got used to it after a few hours.
  * Mac only dev platform means shelling cash to purchase a Macbook just to try writing for iPhone

![http://i.imgur.com/Tibl8.png](http://i.imgur.com/Tibl8.png)

Total development time: 5 hours.

# Android #

  * IDE: Eclipse, [Android SDK 2.1](http://developer.android.com/sdk/)
  * Language: Java
  * Twitter lib: [twitter4j](http://twitter4j.org/)
  * Development platform: Windows, Mac, Linux
  * Emulator is more flexible compared to iPhone, screen size scalable, however while its Xemu VM emulate more accurately, it's slow.
  * Eclipse run slowly on Mac, much faster in Windows
  * Documentation is not as easy to access as XCode
  * Coming from C# developer, Java syntax is super friendly compared to Objective-C

![http://i.imgur.com/X6d18.png](http://i.imgur.com/X6d18.png)
![http://i.imgur.com/Mce8Q.png](http://i.imgur.com/Mce8Q.png)

Total development time: 4.5 - 5 hours, mostly caused by difficulties in [writing asynchronous twitter4j](http://twitter4j.org/en/code-examples.html#asyncAPI) (as opposed to MGTwitterEngine which is pretty straightforward).

# Blackberry #

  * IDE: Eclipse, using [BlackBerry Java Plug-in](http://www.google.com/search?btnI=&q=blackberry+plug-in+eclipse)
  * Language: Java ME
  * Twitter lib: ripped from [Jibjib](http://sugree.com/project/jibjib) application
  * Development platform: Windows, Mac
  * Simulator must be rebooted on every deployment, and it can takes a long time (like rebooting a real BB device)
  * Difficulties in finding existing library that works on Java ME
  * BB only includes subset of the full standard JME libraries
  * Surprisingly snappy UI performance, in addition to standard feel, however it can be pretty difficult to differentiate the apps

![http://i.imgur.com/bnhnb.png](http://i.imgur.com/bnhnb.png)

Total development time: 7.5 hours, mostly caused by debugging network codes, and I don't think all of the issues are solved.

# Maemo #

  * IDE: [ESBox](http://www.google.com/search?btnI=&q=maemo+esbox)
  * Language: Python (Maemo supports a lot of language including C, C++, Python, Ruby, etc), GTK+
  * Twitter lib: [python-twitter](http://code.google.com/p/python-twitter/), the same one I used for base line app, no modification at all!
  * Development platform: Linux only ([complete VM Image is provided](http://www.google.com/search?btnI=&q=maemo+virtual+image) to run on any platform that can run the vm)
  * Simulator never needs restarting on each deployment, and it's pretty fast too, maybe the fastest.
  * Build time is super fast, though using Python might be the factor :)
  * Hildon (the UI engine) is simply stunning
  * My most favorite development environment, though Python support might be the factor as well :)
  * Too bad Nokia has disbanded Maemo! Good thing Intel pickup the left over and commit to continue its development (changed the name to MeeGo)

![http://i.imgur.com/7VPiP.png](http://i.imgur.com/7VPiP.png)
![http://i.imgur.com/jwZig.png](http://i.imgur.com/jwZig.png)

Total development time: 3 hours.

# Symbian S60 3rd edition FP2 #

  * IDE: [Carbide C++](http://www.google.com/search?btnI=&q=Carbide+C%2B%2B)
  * Language: C++ (also support Java ME, and Python), QT framework for UI, Network, and XML
  * Twitter lib: [twitcurl](http://code.google.com/p/twitcurl/) (FAILED!), [QTwitLib](http://code.google.com/p/twitlib/)
  * Development Platform: Windows only
  * Simulator must be rebooted on each deployment, reboot time is a litte bit faster than BB, but the overall performance is sluggish.
  * The C++ does not include standard library, there is no string, I repeat, string is not available! Something called "Descriptor" supposedly replaces string, but its fking difficult to use! Fortunately, QT provides string.
  * Terms used in QT are confusing if you have not used it before since QT is targeted for multiple desktop-based platforms and just recently been brought to mobile environment. E.g. QT Toolbar, in mobile device?
  * QT high learning curve since it totally replaces all standard Symbian UI kit, you need to relearn developing UI for QT.
  * C++ is difficult to get right, and combined with the other issues, this is the one mobile platform I least enjoy.

![http://i.imgur.com/K1iQ0.png](http://i.imgur.com/K1iQ0.png)
![http://i.imgur.com/zVDWb.png](http://i.imgur.com/zVDWb.png)

Total development time: 12 hours (7 hours caused by having to redo development using QT).

Note: early 2011 was the coming of news about [Nokia abandoning QT development](http://www.google.com/search?btnI=&q=Nokia+abandon+qt) and Symbian altogether. Relating to my negative experience in developing on this platform, can there be a lesson learned here?

# Windows Mobile 6 #

  * IDE: Visual Studio 2008
  * Language: C#, .NET Compact 3.5
  * Twitter lib: [tweetsharp](http://tweetsharp.codeplex.com/)
  * Coming from C# developer, it's practically been a zero learning curve. I really feel at home on this platform.
  * Great IDE, the UI designer is as good as XCode, maybe the best IDE.
  * Simulator does not need rebooting on each deployment, but start up time can be lengthy, and the UI is not quite responsive.

![http://i.imgur.com/31cZZ.png](http://i.imgur.com/31cZZ.png)

Total development time: 1 hour 13 minutes, though maybe I got lucky since tweetsharp had sample codes that do just what I needed.