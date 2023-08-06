from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import pytz
import re


def to_text(html):
  return re.sub('[ \t]+', ' ', strip_tags(html)).replace('\n ', '\n').strip()


def color(alternate):
  if alternate:
    return "#1EA5B3"
  else:
    return "#F39200"

class Command(BaseCommand):
  help = 'I will send a digest.'

  def add_arguments(self, parser):
    parser.add_argument(
        "--dry-run",
        default=False,
        nargs="?",
        const=True,
        help="Do not send any mail",
    )

  def handle(self, *args, **options):
    # Set datetime, 7 days in past, UTC-based
    delta = pytz.UTC.localize(datetime.now() - timedelta(7))
    failure = 0
    total = 0

    # Ensure the user accept to receive emails
    for user in get_user_model().objects.all():
      if hasattr(user, 'settings'):
        if user.settings.receiveMail:
          message_html = ""
          alternate = 0

          # The circles container from an user only contains circlememberships
          for circlemember in user.circles.all():
            circle = circlemember.circle
            polls_html = ""
            resources_html = ""
            events_html = ""

            if hasattr(circle, 'polls'):
              polls = circle.polls.get_queryset().filter(~Q(author=user), creationDate__gte=delta).order_by('-creationDate')
              for poll in polls:
                alternate = not alternate
                polls_html += render_to_string('digest/poll.html', {"poll": poll, "color": color(alternate)})
              if polls_html != "":
                polls_html = render_to_string('digest/polls.html', {
                  "circle": circle,
                  "count": polls.count(),
                  "content": polls_html
                })

            if hasattr(circle, 'resources'):
              resources = circle.resources.get_queryset().filter(~Q(user=user), creationDate__gte=delta)
              for resource in resources:
                alternate = not alternate
                resources_html += render_to_string('digest/resource.html', {"resource": resource, "color": color(alternate)})
              if resources_html != "":
                resources_html = render_to_string('digest/resources.html', {
                  "circle": circle,
                  "count": resources.count(),
                  "content": resources_html
                })

            if hasattr(circle, 'events'):
              events = circle.events.get_queryset().filter(~Q(author=user), creationDate__gte=delta)
              for event in events:
                alternate = not alternate
                events_html += render_to_string('digest/event.html', {"event": event, "color": color(alternate)})
              if events_html != "":
                events_html = render_to_string('digest/events.html', {
                  "circle": circle,
                  "count": events.count(),
                  "content": events_html
                })

            if polls_html or resources_html or events_html:
              message_html += render_to_string('digest/circle.html', {
                "circle": circle,
                "polls": polls_html,
                "events": events_html,
                "resources": resources_html
              })
            
          if message_html != "":
            message_html = render_to_string('digest/circles.html', {
              "content": message_html
            })

          inbox_html = ""
          inbox_mentions = user.inbox.get_queryset().filter(date__gte=delta, type="Mention").count()
          if inbox_mentions > 0:
            inbox_html += render_to_string('digest/inbox_mentions.html', {
              "count": inbox_mentions
            })
          inbox_messages = user.inbox.get_queryset().filter(date__gte=delta, type="Message").count()
          if inbox_messages > 0:
            inbox_html += render_to_string('digest/inbox_messages.html', {
              "count": inbox_messages
            })
          if inbox_html != "":
            message_html += render_to_string('digest/inbox.html', {
              "inbox_messages": inbox_messages,
              "inbox_mentions": inbox_mentions,
            })


          all_votes_html = ""
          for poll in user.createdVotes.all():
            votes = poll.votes.get_queryset().filter(creationDate__gte=delta).order_by('-creationDate')
            votes_html = ""
            for vote in votes:
              if vote.user != user:
                votes_html += render_to_string('digest/vote.html', {"vote": vote})
            if votes_html != "":
              alternate = not alternate
              all_votes_html += render_to_string('digest/votes.html', {
                "poll": poll,
                "count": votes.count(),
                "content": votes_html,
                "color": color(alternate)
              })
          if all_votes_html != "":
            message_html += render_to_string('digest/votes_heading.html', {
              "content": all_votes_html
            })


          if message_html != "":
            message_html = render_to_string('digest/template.html', {"settings": settings, "user": user, "content": message_html})
            total = total + 1
            if(options["dry_run"]):
              self.stdout.write(self.style.SUCCESS(user.urlid))
              self.stdout.write(message_html)
            else:
              try:
                send_mail(
                    'Votre semaine sur la République de l\'ESS',
                    to_text(message_html),
                    (getattr(settings, 'DEFAULT_FROM_EMAIL', False)\
                      or getattr(settings, 'EMAIL_HOST_USER', False)\
                      or "noreply@" + settings.JABBER_DEFAULT_HOST),
                    [user.email],
                    fail_silently = False,
                    html_message = message_html
                )
                self.stdout.write(self.style.SUCCESS('Sent digest to ' + user.email))
              except:
                failure = failure + 1
                self.stdout.write(self.style.WARNING('Unable to send digest to ' + user.email))

    if(options["dry_run"]):
      self.stdout.write(self.style.SUCCESS('Digest done. Generated: ' + str(total)))
    else:
      self.stdout.write(self.style.SUCCESS('Digest done. Sent: ' + str(total - failure) + '/' + str(total)))
