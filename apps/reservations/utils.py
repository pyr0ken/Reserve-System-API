from datetime import date, datetime

def datetime_to_timestamp(date, time):
    # تبدیل تاریخ و زمان به timestamp
    datetime_str = f'{date} {time}'
    dt_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    timestamp = dt_object.timestamp()
    return int(timestamp)

def timestamp_to_datetime(timestamp):
    # تبدیل timestamp به تاریخ و زمان
    dt_object = datetime.fromtimestamp(int(timestamp))
    return dt_object.date(), dt_object.time()
