import datetime
#date_format : %Y-%m-%d   ||   '%d-%b-%Y'
def get_curr_date():
    return datetime.datetime.strftime(datetime.datetime.today(),  "%Y-%m-%d")

#-----------------------#   "%A %d %B %Y %I:%M:%S%p" ===> Tuesday 09 April 2019 03:39:05PM
#  Get current datetime #
#-----------------------#
def get_curr_datetime_without_format():
    return datetime.datetime.now()
def get_curr_datetime():
    # --> https://stackoverflow.com/questions/25837452/python-get-current-time-in-right-timezone
    utc_dt = datetime.datetime.now(datetime.timezone.utc) # UTC time
    return datetime.datetime.strftime(utc_dt.astimezone(),"%Y-%m-%d %H:%M:%S%z") # local time
    #return utc_dt.astimezone() # local time
    # datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p") # Without considering UTC

    # WORKABLE IN PC : https://stackoverflow.com/questions/2720319/python-figure-out-local-timezone
    #LOCAL_TIMEZONE = datetime.datetime.now().astimezone().tzinfo
    #return datetime.datetime.strftime(datetime.datetime.now(LOCAL_TIMEZONE),"%Y-%m-%d %H:%M:%S%z")
    #return datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S-%z")
# https://stackoverflow.com/questions/2331592/why-does-datetime-datetime-utcnow-not-contain-timezone-information
# https://stackoverflow.com/questions/13182075/how-to-convert-a-timezone-aware-string-to-datetime-in-python-without-dateutil
# https://stackoverflow.com/questions/3305413/python-strptime-and-timezones
def get_curr_datetime_in_utc():
    return datetime.datetime.strftime(datetime.datetime.now(datetime.timezone.utc),"%Y-%m-%d %H:%M:%S%z")

#===========================#
#  Convert String to Date   #
#===========================#
def convert_str_to_date (date_text):
    try:
        convert_date = datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return None
    else:
        return convert_date

def convert_str_to_datetime (datetime_text):
    try:
        convert_date = datetime.datetime.strptime(datetime_text, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None

    else:
        return convert_date


#====================#  https://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python
#  Time difference   #  https://stackoverflow.com/questions/19472859/python-convert-datetime-formatted-string-to-seconds
#====================# 
def get_time_difference_in_sec(time1_in_utc, time2_in_utc):
    duration = datetime.datetime.strptime(time2_in_utc, "%Y-%m-%d %H:%M:%S%z") - datetime.datetime.strptime(time1_in_utc, "%Y-%m-%d %H:%M:%S%z")
    return duration.total_seconds()