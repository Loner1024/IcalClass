from requests_html import HTML, HTMLSession
from datetime import datetime, timedelta


class GetIcal(object):
    def __init__(self, student_id):
        self.student_id = student_id

    def get_class(self):
        class_data = []
        class_data_name = []
        class_data_week = []
        class_data_time = []
        class_data_place = []
        session = HTMLSession()
        session.get('https://www.shzurk.com/ThinkYibanclass/index.php/Main/index?username=loner&studentid=%s' % self.student_id)
        r = session.get('https://www.shzurk.com/ThinkYibanclass/index.php/Main/myClass')
        class_data_name = r.html.find('.kcmc')
        class_data_week = r.html.find('.skzs')
        class_data_time = r.html.find('.xq')
        class_data_place = r.html.find('.dd')

        def deal_data(class_info):
            for i in range(len(class_info)):
                class_info[i] = class_info[i].text
             
        deal_data(class_data_name)
        deal_data(class_data_week)
        deal_data(class_data_time)
        deal_data(class_data_place)

        for i in range(len(class_data_name)):
            class_list = [class_data_name[i],class_data_week[i],class_data_time[i],class_data_place[i]]
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

            if len(i[1]) <= 2:
                i[1] = [int(i[1])]
            if len(i[1]) = 3:
                i[1] = []
                                

        print(self.class_data)


if __name__ == "__main__":
    x = TimeList(20190304, 20190901)
    # x.time_list()
    y = GetIcal('20171016087')
    # y.get_class()
    z = MergeData(y.get_class(),x.time_list())
    z.merge_data()