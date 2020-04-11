# Lys

![Deploy lambda](https://github.com/corentindautreme/lys/workflows/Deploy%20lambda/badge.svg)

Lys is a [Twitter bot](https://twitter.com/EurovisionLys) aiming at publishing daily reminders for every Eurovision national selection show happening in Europe (and Australia).

## What does it do exactly?

Twice a day, this script will be run and search for events (selection shows) happening on the day in a manually maintained database (although most events are extracted automatically, take a look [over there](https://github.com/corentindautreme/lys-event-fetcher)).

For each event found, the bot will post a Tweet on the @EurovisionLys twitter account.

## How does it run?

* The script is run using an AWS Lambda
* Events are stored in a AWS DynamoDB table

## Dependencies

* [Tweepy](https://github.com/tweepy/tweepy)