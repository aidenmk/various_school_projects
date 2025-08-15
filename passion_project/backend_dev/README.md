# In Progress Passion Project
This is a snippet of my in progress passion project where I plan to make a model that estimates ideal watering interval for bonsai tree watering. It is quite a mess right now since it is in progress and I am trying to find time to work on it and learn by doing. I am mostly adding this to git to showcase my ability.

In short, what the goal of this project is, is to take in various variables such as temp, humidity, altitude, species type, potted soil type, last watering time, etc... and output is an optimal watering interval.

Since there is no formal database of these properties and watering interval, I have to make the database with the data I have found. Specifically, I webscraped from the USDA plants database to find relevant properties.

Since I am learning by doing, I realized that USDA actually has an api and I didn't need to use selenium to click thousands of buttons on their website overnight while I was sleeping for 4 hours (sorry USDA plants database D:).

Anywho, check out bootstrapplant.py if you want to see the self created database being made. I have yet to tune up the conditionals in that file to find a realistic watering interval. I hope to get it working soon so that way I have data to train up (and learn more about) a supervised or unsupervised model.

Another portion I've been working on that is not published here is setting up an api using aws lambda to relay info from backend to frontend.

Future plans are to create a mobile app.


