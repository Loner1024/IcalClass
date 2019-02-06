from datetime import datetime,timedelta

start_time = datetime.strptime('20190301','%Y%m%d')
end_time = datetime.strptime('20190701','%Y%m%d')
time_list = [[],[],[],[],[],[],[]]
now = datetime.now()

while start_time != end_time:
    if start_time == end_time:
        break
    else:
        if start_time.weekday() == 0:
            time_list[0].append(start_time.strftime('%Y%m%d'))
        elif start_time.weekday() == 1:
            time_list[1].append(start_time.strftime('%Y%m%d'))
        elif start_time.weekday() == 2:
            time_list[2].append(start_time.strftime('%Y%m%d'))
        elif start_time.weekday() == 3:
            time_list[3].append(start_time.strftime('%Y%m%d'))
        elif start_time.weekday() == 4:
            time_list[4].append(start_time.strftime('%Y%m%d'))
        elif start_time.weekday() == 5:
            time_list[5].append(start_time.strftime('%Y%m%d'))
        elif start_time.weekday() == 6:
            time_list[6].append(start_time.strftime('%Y%m%d'))
        start_time = start_time + timedelta(days=1)

print(time_list[6])


