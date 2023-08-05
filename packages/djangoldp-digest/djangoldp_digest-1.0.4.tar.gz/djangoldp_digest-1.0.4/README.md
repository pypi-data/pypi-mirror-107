# DjangoLDP Digest

ESS france specific package. Require [Generic branding](https://git.startinblox.com/management/startinblox-feature-requests/issues/243) to allow other customer to take benefits.

Package contain a command that send a relevant digest to every users regarding actions on their Circles, Events, Polls, Resources and Votes.

To run the command:

```bash
python manage.py digest
```

You can dry run the command, avoiding to send emails, with:

```bash
python manage.py digest --dry-run
```

This package assume that you're running on a DjangoLDP server with proper packages & configured to send emails.
