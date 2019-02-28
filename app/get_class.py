from requests_html import HTML, HTMLSession
from datetime import datetime, timedelta
import uuid
import tempfile, os
from icalendar import Calendar, Event, vText


class GetIcal(object):
    def __init__(self, student_id):
        self.student_id = student_id

    def get_class(self):
        class_data = []
        class_data_name = []
        class_data_week = []
        class_data_time = []
        class_data_place = []
        class_data_lesson = []
        session = HTMLSession()
        session.get('https://www.shzurk.com/ThinkYibanclass/index.php/Main/index?username=loner&studentid=%s' % self.student_id)
        r = session.get('https://www.shzurk.com/ThinkYibanclass/index.php/Main/myClass')
        class_data_name = r.html.find('.kcmc')
        class_data_week = r.html.find('.skzs')
        class_data_time = r.html.find('.xq')
        class_data_place = r.html.find('.dd')
        class_data_lesson = r.html.find('.jc')

        def deal_data(class_info):
            for i in range(len(class_info)):
                class_info[i] = class_info[i].text
             
        deal_data(class_data_name)
        deal_data(class_data_week)
        deal_data(class_data_time)
        deal_data(class_data_place)
        deal_data(class_data_lesson)

        for i in range(len(class_data_name)):
            class_list = [class_data_name[i], class_data_week[i], class_data_time[i], class_data_place[i],class_data_lesson[i]]
            class_data.append(class_list)
        return class_data


class TimeList(object):
    def __init__(self, start_time, end_time):
        self.start_time = datetime.strptime(str(start_time), '%Y%m%d')
        self.end_time = datetime.strptime(str(end_time), '%Y%m%d')

    def time_list(self):
        all_week_list = []
        week_list = []
        while self.start_time != self. end_time:
            self.start_time += timedelta(days = 1)
            week_list.append(self.start_time.strftime('%Y%m%d'))
            if self.start_time.weekday() == 6:
                all_week_list. append(week_list)
                week_list = []
            else:
                continue
        return all_week_list


class MergeData(object):
    def __init__(self, class_data, all_week_list):
        self.class_data = class_data
        self.all_week_list = all_week_list

    def merge_data(self):
        for i in self.class_data:
            if i[2] == '星期一':
                i[2] = 0
            elif i[2] == '星期二':
                i[2] = 1
            elif i[2] == '星期三':
                i[2] = 2
            elif i[2] == '星期四':
                i[2] = 3
            elif i[2] == '星期五':
                i[2] = 4
            elif i[2] == '星期六':
                i[2] = 5
            elif i[2] == '星期天':
                i[2] = 6
            
            if i[4] == '1-2':
                i[4] = [1000, 1140]
            elif i[4] == '3-4':
                i[4] = [1210, 1350]
            elif i[4] == '5-6':
                i[4] = [1600, 1740]
            elif i[4] == '7-8':
                i[4] = [1800, 1940]
            elif i[4] == '9-10':
                i[4] = [2030, 2210]
            elif i[4] == '1-4':
                i[4] = [1000, 1350]
            elif i[4] == '5-8':
                i[4] = [1600, 1940]
            elif i[4] == '7-10':
                i[4] = [1800, 2210]

            week = i[1]
            week = week.split(',')
            week_1 = []
            week_2 = []
            for k in week:
                k = k.split('-')
                for n in range(len(k)):
                    k[n] = int(k[n])
                week_1.append(k)
            for k in week_1:
                for z in range(k[0],k[-1]+1):
                    week_2.append(z)
            i[1] = week_2

            for k in range(len(i[1])):
                i[1][k] = self.all_week_list[i[1][k]][2]
                # print(i[1])
        return(self.class_data)

class OutIcal(object):
    def __init__(self, class_data, student_id):
        self.class_data = class_data
        self.student_id = student_id

    def out_ical(self):
        cal = Calendar()
        cal.add('prodid', '-//My calendar product//mxm.dk//')
        cal.add('version', '2.0')
        n = 0
        for ical_data in self.class_data:
            for i in range(len(ical_data[1])):
                event = Event()
                event.add('summary', ical_data[0])
                print(str(ical_data[4][0]))
                event.add('dtstart', datetime.strptime(ical_data[1][i] + str(ical_data[4][0]), '%Y%m%d%H%M'))
                event.add('dtend', datetime.strptime(ical_data[1][i]+str(ical_data[4][1]),'%Y%m%d%H%M'))
                event.add('dtstamp', datetime.strptime(ical_data[1][i]+str(ical_data[4][0]),'%Y%m%d%H%M'))
                event['location'] = vText(ical_data[3])
                event['uid'] = uuid.uuid1()
                cal.add_component(event)
                # directory = tempfile.mkdtemp()
        cwd = os.getcwd()
        os.chdir(cwd + '/app/static/ical_file/')
        f = open(os.path.join(self.student_id + '.ics'), 'wb')
        f.write(cal.to_ical())
        f.close()
            

'''
if __name__ == '__main__':
    x = TimeList(20190303, 20190901)
    #print(x.time_list()) 
    y = GetIcal('20181014023')
    #y = GetIcal('20171016087')
    #print(y.get_class())
    z = MergeData(y.get_class(), x.time_list())
    #print(z.merge_data()[7])
    k = OutIcal(z.merge_data(), '20181014023')
    k.out_ical()
'''