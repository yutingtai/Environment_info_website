from django.core.management.base import BaseCommand

from display_info.models import EqDataDbModel, IntensityDbModel, AqiDataDbModel


def do_delete():
    EqDataDbModel.objects.all().delete()
    IntensityDbModel.objects.all().delete()
    AqiDataDbModel.objects.all().delete()


class Command(BaseCommand):
    help = "Drops all data from database"

    def handle(self, *args, **options):
        do_delete()
