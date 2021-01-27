from crontab import CronTab

cron = CronTab(user='username')
index = cron.new(command='python monitor.py')

index.hour.on(9)
index.week.on('FRI', 'MON')

cron.write()

#0 9 * * 6 python monitor.py
