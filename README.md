# sebot

A simple Slackbot that reflects @channel mentions to e-mail.

## Prerequisites

* Python 2.7
* An API token from a Slack instance
* Crontab access

## Setup

Install Slack API library.

```
  pip install -r requirements.txt
```

Copy `credentials-template.py` to `credentials.py`.

```
  cp credentials-template.py credentials.py
```

Edit `credentials.py` to reflect reality.

Add sebot.py to crontab so it runs every 5 minutes.

```
  PATH=/path/to/python
  */5 * * * * cd /path/to/sebot && python sebot.py
```

Profit!
