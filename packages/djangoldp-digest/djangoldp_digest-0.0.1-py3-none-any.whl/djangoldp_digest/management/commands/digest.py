from django.core.management.base import BaseCommand

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

    self.stdout.write(self.style.SUCCESS('Burb.'))
