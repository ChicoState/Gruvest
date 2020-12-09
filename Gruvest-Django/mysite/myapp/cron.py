import datetime

def update_stock_objects():
    #Zero: in settings.py look for CRONJOBS to adjust frequency of updates
    #format is "minutes(0-59) hours(0-23) days(1-31) months(1-12) weekday(0-6)"
    #Ex. 0 9-17 1-21 1-6 *
    #Means at minute 0, for every hour between 9:00 to 17:00, for the first 21 days of the month, for the months January through June, ANY (wildcard *) day of the week
    #run $ python manage.py crontab add
	#anytime you want to add defined cronjobs in settings.py to crontab util
	#crontab show to display CRONJOBS, and crontab remove to remove jobs from crontab
    print("It is now ", datetime.datetime.now().strftime("%H:%M:%S"))
