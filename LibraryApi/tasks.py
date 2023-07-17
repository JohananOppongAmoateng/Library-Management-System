from celery import shared_task
from .models import Borrowing,Fine
from datetime import datetime

fine = 0.2

@shared_task(name="fine-defaulters")
def fine_defaulters():
    defaulted = Borrowing.objects.filter(returned=False,due_date__lt=datetime.now())
    for i in defaulted:
        fine = Fine.objects.get
        # if defaulters.
    

