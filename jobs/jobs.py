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
            print(difference_days, query)
            if difference_days > 0.019 and difference_days < 0.022:
                query.is_active = False
                query.save()

