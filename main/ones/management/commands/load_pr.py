from django.core.management.base import BaseCommand
from django.utils import timezone
from ones.views import ones

class Command(BaseCommand):
    help = 'Отображает текущее время'
    def handle(self, *args, **kwargs):
        ones()