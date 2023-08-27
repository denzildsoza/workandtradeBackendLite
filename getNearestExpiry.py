import pandas as pd
from datetime import timedelta, date, datetime
from calendar import day_name

def getNextWeaklyEpiry():
    today = date.today()
    daysaHead = (3 - today.weekday()) % 7
    nearestExpiry = today + timedelta(days=daysaHead)
    return nearestExpiry
print(getNextWeaklyEpiry())
expiry_date_epoch = int(
                    (
                        datetime.strptime(
                            f"{getNextWeaklyEpiry()} 20:00:00", "%Y-%m-%d %H:%M:%S"
                        )
                    ).timestamp()
                )
print(expiry_date_epoch)