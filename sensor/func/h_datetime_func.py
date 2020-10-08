import datetime
#date_format : %Y-%m-%d   ||   '%d-%b-%Y'
def get_curr_date():
    return datetime.datetime.strftime(datetime.datetime.today(),  "%Y-%m-%d")

#-----------------------#   "%A %d %B %Y %I:%M:%S%p" ===> Tuesday 09 April 2019 03:39:05PM
#  Get current datetime #
#-----------------------#
def get_hour():
    return datetime.datetime.now().hour

def get_curr_datetime_without_format():
    return datetime.datetime.now()

def get_curr_datetime():
    # --> https://stackoverflow.com/questions/25837452/python-get-current-time-in-right-timezone
    utc_dt = datetime.datetime.now(datetime.timezone.utc) # UTC time
    return datetime.datetime.strftime(utc_dt.astimezone(),"%Y-%m-%d %H:%M:%S%z") # local time
    
def get_curr_datetime_in_utc():
    return datetime.datetime.strftime(datetime.datetime.now(datetime.timezone.utc),"%Y-%m-%d %H:%M:%S%z")


#====================#  https://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python
#  Time difference   #  https://stackoverflow.com/questions/19472859/python-convert-datetime-formatted-string-to-seconds
#====================# 
def get_time_difference_in_sec(time1_in_utc, time2_in_utc):
    duration = datetime.datetime.strptime(time2_in_utc, "%Y-%m-%d %H:%M:%S%z") - datetime.datetime.strptime(time1_in_utc, "%Y-%m-%d %H:%M:%S%z")
    return duration.total_seconds()