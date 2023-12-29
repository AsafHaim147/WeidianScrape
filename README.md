# WeidianScrape
A multi-store scraper for weidian stores. Using Selenium on Python you can scrape multiple stores, gaining real-time information regarding items name, price and picture straight into your telegram bot. Making deal hunting ridiculously easy.

This scraper is based on Selenium because BS4 had some issues decoding chinese text. interested in a BS4 version? check this : https://github.com/AsafHaim147/SBMonitor

####  BEFORE STARTING:
This simple program was made for personal,fair and legal use. Please avoid abusing websites with it. 
I left all the information on purpose so beginner developers could reverse engineer the things they didn't fully understand even though this is a pretty simple Selenium script.

There are two possible ways of using it: 
1. Replacing the links and supplier names on config.py and running weidian.py
2. (Recommended) deleting everything on assets.json, which means you will have to run feeder.py first in order to get a starting image of your database before monitoring.
   I was lazy and decided not to fix this because when using feeder.py for testing I realized that it's also a nice solution and also a nice demo of how the scraping works so you can make your own changes before monitoring
   


SET-UP:
1. Create a telegram bot at https://core.telegram.org/bots/tutorial
2. Fill Bot API and chat ID in config.py
3. Change your supplier link and name Correspondinly, for exmaple:
   ['Link1','Link2','Link3']
   ['Supplier1','Supplier2','Supplier3']
4. That's it! run weidian.py (after completing the steps at lines 11-12) and wait for those messages!
