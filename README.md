# Lys

[![Deploy lambdas](https://github.com/corentindautreme/lys/actions/workflows/publish_lambda.yml/badge.svg)](https://github.com/corentindautreme/lys/actions/workflows/publish_lambda.yml)

Lys is a bot for [Bluesky](https://bsky.app/profile/eurovisionlys.bsky.social), [Twitter](https://x.com/EurovisionLys), and [Threads](https://www.threads.net/@eurovisionlys) aiming at publishing daily reminders for every Eurovision national selection show happening in Europe (and Australia).

## What does it do exactly?

Twice a day, a script will be run and search for events (selection shows) happening on the day in a manually maintained database (although most events are extracted automatically, take a look [over there](https://github.com/corentindautreme/lys-event-fetcher)). For each event found, the bot will publish a post that looks just like this:

> TONIGHT | 🇸🇪 SWEDEN<br>
\---------<br>
📼 Melodifestivalen<br>
🏆 Final<br>
🕓 20:00 CET<br>
\---------<br>
 📺 https://svtplay.se.

There is also a weekly post every Sunday afternoon that contains a summary of the week ahead:

> 🗓️ COMING UP NEXT WEEK (* = final):<br><br>
 \- Tuesday 16: 🇪🇪<br>
 \- Thursday 18: 🇪🇪<br>
 \- Saturday 20: 🇸🇪🇳🇴*

And finally, a reminder for every show 5 minutes before they start:

> 🚨 5 MINUTES REMINDER!<br>
\---------<br>
🇸🇪 Melodifestivalen - Heat 2 (https://svtplay.se/melodifestivalen)<br>
\---------<br>
🇳🇴 Melodi Grand Prix - Final (https://nrk.no/mgp)

## How does it run?

* The main entrypoint, `lys.py`, is launched as an AWS Lambda, with different arguments depending on the target mode (daily thread, weekly post, 5-minute reminders) and platform (Bluesky, Twitter, or Threads)
* Events are stored in a AWS DynamoDB table

## Dependencies

* [Tweepy](https://github.com/tweepy/tweepy)