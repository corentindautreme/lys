# Lys

![Deploy lambda](https://github.com/corentindautreme/lys/workflows/Deploy%20lambda/badge.svg)

Lys is a [Twitter bot](https://twitter.com/EurovisionLys) aiming at publishing daily reminders for every Eurovision national selection show happening in Europe (and Australia).

## What does it do exactly?

Twice a day, this script will be run and search for events (selection shows) happening on the day in a manually maintained database (although most events are extracted automatically, take a look [over there](https://github.com/corentindautreme/lys-event-fetcher)). For each event found, the bot will post on the @EurovisionLys twitter account a Tweet that looks just like this:

> TONIGHT: 🇸🇪 Sweden | Melodifestivalen - Final at 20:00 CET. Watch live: https://svtplay.se

There is also a weekly tweet every Sunday afternoon that contains a summary of the week ahead:

> Coming up next week (* = final):<br>
 \- Tuesday: 🇪🇪<br>
 \- Saturday: 🇸🇪🇳🇴*

And finally, a reminder for every show 5 minutes before they start:

> (format to be defined)

## How does it run?

* There is one script per update (the 2 times daily update, weekly update and 5 minute reminder)
* The scripts are run using AWS Lambdas
* Events are stored in a AWS DynamoDB table

## Dependencies

* [Tweepy](https://github.com/tweepy/tweepy)