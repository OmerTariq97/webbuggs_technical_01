
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import testfunc

def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_jobstore(DjangoJobStore(), 'default')
    # scheduler.add_job(testfunc, 'interval', seconds=5, args = ["Specified time!"])
    # scheduler.start()