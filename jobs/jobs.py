import datetime
import pytz
import datetime

from accounts.models import User
def testfunc(self):
    queryset = User.objects.all()
    for query in queryset:
        if query.last_login:
            today = datetime.datetime.now()
            zero_offset = datetime.timedelta(0)
            today_utc = today.replace(tzinfo=pytz.utc) - zero_offset
            difference = today_utc - query.last_login
            difference_days = difference.total_seconds()/86400
            print('start')
            if difference_days > 30:
                query.is_active = False
                query.save()

