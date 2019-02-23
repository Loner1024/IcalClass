import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os

class_data = []


class GetIcal(object):
    def __init__(self, student_id):
        self.student_id = student_id

    def get_class(self):

        class_data_name = []
        class_data_week = []
        class_data_time = []
        class_data_place = []
        s = requests.Session()
        s.get('https://www.shzurk.com/ThinkYibanclass/index.php/Main/index?username=loner&studentid=%s' % self.student_id)
        r = s.get(
            "https://www.shzurk.com/ThinkYibanclass/index.php/Main/myClass").text
        data_name = BeautifulSoup(r, 'lxml').select('div.major > p.kcmc')
        data_week = BeautifulSoup(r, 'lxml').select('div.major > p.xq')
        data_time = BeautifulSoup(r, 'lxml').select('div.major > p.jc')
        data_place = BeautifulSoup(r, 'lxml').select('div.major > p.dd')

        def deal_data(class_info, out_data):
            for data in class_info:
                text = data.get_text()
                out_data.append(text)

        def deal_time(class_data):
            start_time = datetime.strptime('20190301', '%Y%m%d')
            end_time = datetime.strptime('20190901', '%Y%m%d')
            time_list = [[], [], [], [], [], [], []]
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

            for i in range(len(class_data)):
                if class_data[i]['class_week'] == '星期一':
                    class_data[i]['class_week'] = time_list[0][i]
                elif class_data[i]['class_week'] == '星期二':
                    class_data[i]['class_week'] = time_list[1][i]
                elif class_data[i]['class_week'] == '星期三':
                    class_data[i]['class_week'] = time_list[2][i]
                elif class_data[i]['class_week'] == '星期四':
                    class_data[i]['class_week'] = time_list[3][i]
                elif class_data[i]['class_week'] == '星期五':
                    class_data[i]['class_week'] = time_list[4][i]
                elif class_data[i]['class_week'] == '星期六':
                    class_data[i]['class_week'] = time_list[5][i]
                elif class_data[i]['class_week'] == '星期天':
                    class_data[i]['class_week'] = time_list[6][i]

            for i in range(len(class_data)): 
                if class_data[i]['class_time'] == '1-2':
                    class_data[i]['class_time'] = [100000, 114000]
                elif class_data[i]['class_time'] == '3-4':
                    class_data[i]['class_time'] = [121000, 135000]
                elif class_data[i]['class_time'] == '5-6':
                    class_data[i]['class_time'] = [160000, 174000]
                elif class_data[i]['class_time'] == '7-8':
                    class_data[i]['class_time'] = [180000, 194000]
                elif class_data[i]['class_time'] == '9-10':
                    class_data[i]['class_time'] = [203000, 221000]

        deal_data(data_name, class_data_name)
        deal_data(data_week, class_data_week)
        deal_data(data_time, class_data_time)
        deal_data(data_place, class_data_place)
        for n in range(0, len(class_data_name)):
            class_list = {'class_name': class_data_name[n], 'class_week': class_data_week[n],
                          'class_time': class_data_time[n], 'class_place': class_data_place[n]}
            n = n+1
            class_data.append(class_list)
        deal_time(class_data)
        return class_data
            
    def out_ical(self, ical_class):
        with open(self.student_id + '.ics', 'ab') as f:
            f.write('BEGIN:VCALENDAR\n'.encode(encoding='utf-8'))
            f.write('PRODID:-//Loner//SHZU//\n'.encode(encoding='utf-8'))
            f.write('VERSION:2.0\n'.encode(encoding='utf-8')) # 遵循的 iCalendar 版本号
            f.write('CALSCALE:GREGORIAN\n'.encode(encoding='utf-8')) # 使用公历
            f.write('X-WR-CALNAME:课程表\n'.encode(encoding='utf-8'))
            f.write('X-WR-TIMEZONE:Asia/Shanghai\n'.encode(encoding='utf-8'))

        for ical in ical_class:
            start_time = 'DTSTART:'+ical['class_week']+'T'+str(ical['class_time'][0])+'Z\n'
            DTSTAMP = 'DTSTAMP:'+ical['class_week']+'T'+str(ical['class_time'][0])+'Z\n'
            UID = 'UID:'+ical['class_week']+'T'+str(ical['class_time'][0])+'Z-SHZU\n'
            end_time = 'DTEND:'+ical['class_week']+'T'+str(ical['class_time'][1])+'Z\n'
            LOCATION = 'LOCATION:'+ical['class_place']+'\n'
            SUMMARY = 'SUMMARY:'+ical['class_name']+'\n'
            with open(self.student_id + '.ics', 'ab') as f:
                f.write('BEGIN:VEVENT\n'.encode(encoding='utf-8')) # 事件开始
                f.write(DTSTAMP.encode(encoding='utf-8')) 
                f.write(start_time.encode(encoding='utf-8')) # 开始时间
                f.write(end_time.encode(encoding='utf-8')) # 结束时间
                f.write(SUMMARY.encode(encoding='utf-8')) # 事件
                f.write(UID.encode(encoding='utf-8'))
                f.write(LOCATION.encode(encoding='utf-8')) # 地点
                f.write('END:VEVENT\n'.encode(encoding='utf-8'))

        with open(self.student_id + '.ics', 'ab') as f:
            f.write('END:VCALENDAR\n'.encode(encoding='utf-8'))