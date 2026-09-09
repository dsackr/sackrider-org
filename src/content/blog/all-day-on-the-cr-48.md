---
title: All Day on the CR-48
description: I spent all day today on the CR-48. There are many challenges to using
  this as your primary (dare I say only) laptop. I left the house this morning to
  head to...
pubDate: '2010-12-29'
draft: true
tags:
- Twitter
---

I spent all day today on the CR-48.  There are many challenges to using this as your primary (dare I say only) laptop.  I left the house this morning to head to a wifi spot so I could get some work done without the children in the back ground.  The library was closed so I headed over to McDonald's.

Getting connected to their wifi was a breeze - I was already logged on to the laptop - so I'm not sure yet how it handled booting up without a wifi connection already setup.  I opened the lid, the laptop came out of standby literally before I could get the lid opened all the way.  I clicked on the wifi icon next to the clock and selected the McD's WAP.  Bam - connected.  I did have to click "I agree... blah blah blah" to use their service, but the laptop had no trouble with that.

On the todo list for the day - migrate several websites from one of my servers to another, create two new websites, catch up on email, keep up on Facebook and Twitter, and possible write a blog post or two.  I had already put the CR-48 into developer mode, although before today I don't think I had a need for it.  I also already knew I could get to a crosh shell that would let me ssh to my servers.  I was ready to get started.

The first thing I notice was that I needed to turn on some kind of music to drown out the McD's chaos.  I don't like Pandora or really any other streaming service out there - plus I have all the songs I love on my phone - but since the laptop only has one USB port - I can't run my phone's media player all day and have my mouse plugged in at the same time (my phone battery would die) - so I quickly jump into the <a href="http://groups.google.com/group/cr-48-test-pilots">Chrome CR-48 Test Pilots Google Group</a>.

There I learn about:flags.  When I type about:flags in the address bar (also known as the omnibar) I get a list of experimental features that are all disabled by default - including "media player" and "advanced filesystem".  I enable both and reboot (takes about 20 seconds or so).  The best part is I was ssh'ed into my server (by hitting Ctrl+Alt+T then typing ssh &lt;username&gt; &lt;server&gt; &lt;port&gt;) - when I "rebooted" to enable the new features, my ssh session did not close - only the Chrome Browser like GUI actually shutdown.

Now I'm able to open the download explorer (Ctrl+O) and see the sdcard where I have put my music.  I can't however browse the sdcard... hmmm... so I drop to a crosh shell and since I'm already in developer mode, I type in shell to get to a bash shell where I can surf to the sdcard and see everything is there.  Using help from the google group, I was able to create a Symbolic link (its like a windows shortcut but for Unix operating systems) in my Downloads folder to the /media folder where the sdcard is mounted.  Now I go back to the browser, hit ctrl+o and start playing music... Awesome!

I do some migration work coping files from one server to another using scp - backup the databases, etc.  I log into cpanel's whm on my server to add a couple of new websites to an existing account, the drop back down to the shell to configure the IP addresses they listen on and install the ssl certs they need for ecommerce.

So far, so good - I take a 'mental' break and jump out to twitter, facebook, and start surfing the google group for more tips.  I create a post asking if anyone knows how to configure my mouse button in ChromeOS (to no avail) and I also comment that I am disappointed with the fact that I can't drag a tab out to a new window in ChromeOS - this is the feature that won me over to Chrome over a year or two ago (has it been that long?!?!).  A few people agree with me but nobody knows if there is a solution on the horizon.

While I was in about:flags I noticed  a "Remoting" option - which I enabled.  Now, under the wrench menu, I have a new "Set up remoting..." option however when I try to set it up - I get authentication errors.  It seems that feature isn't ready for general or even pilot use just yet.

My wife calls - on gtalk.  We have a quick video chat - quality is ok - my wife was in poor lighting and I was in a loud McD's but we were still able to hold a conversation while looking at each other.  After that video call, I thought man it would be cool if I could skype from this thing too.  I jump back in the google group and find out about <a href="https://imo.im/new/">IMO</a>.  It looks pretty cool and I was able to connect to my skype account - and see my contacts - but calling was a no go for me.  I could IM with my contacts, but video and audio calls just didn't work.  It was a good idea - I just couldn't get it to work.

Back to work - it takes me almost an hour <em>after</em> my mental break just to get back on track - during which I am frustrated with the built in mouse pad - its a bit sensitive (although that is adjustable) and often while I'm typing my screen jumps around a bit.  I already disabled tap to click because I was always losing focus (of my cursor - although the pun holds true).

All in all, I had a mostly productive day where I made a lot of progress but didn't get anything done.  Did you catch how many times I had to plug in my laptop?  Don't bother rescanning the post - its not in there because the battery life on this thing is amazing - I'm seeing 8 plus hours from a single charge with this type of usage.

In the future I want to type up a few "how to" articles for the CR-48...
