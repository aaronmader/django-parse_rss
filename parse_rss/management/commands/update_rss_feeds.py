from django.core.management.base import NoArgsCommand

from parse_rss.models import Feed

class Command(NoArgsCommand):
    help = "Fetch rss feeds from remote servers, and update the local copy"

    def handle_noargs(self, **options):
        print "updating feeds..."
        for feed in Feed.objects.all():
            print feed.domain
            feed.update()
