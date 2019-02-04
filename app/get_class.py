import requests
from bs4 import BeautifulSoup
from lxml import etree

class get_ical(object):
    def __init__(self,student_id):
        self.student_id = student_id

    def get_class(self):
        class_data=[]
        class_data_name=[]
        class_data_week=[]
        class_data_time=[]
        class_data_place=[]
        s = requests.Session()
        s.get('https://www.shzurk.com/ThinkYibanclass/index.php/Main/index?username=loner&studentid=%s' %  self.student_id)
        r = s.get("https://www.shzurk.com/ThinkYibanclass/index.php/Main/myClass").text
        data_name = BeautifulSoup(r,'lxml').select('div.major > p.kcmc')
        data_week = BeautifulSoup(r,'lxml').select('div.major > p.xq')
        data_time = BeautifulSoup(r,'lxml').select('div.major > p.jc')
        data_place = BeautifulSoup(r,'lxml').select('div.major > p.dd')
        def deal_data(class_info,out_data):
            for data in class_info:
                text=data.get_text()
                out_data.append(text)
        deal_data(data_name,class_data_name)
        deal_data(data_week,class_data_week)
        deal_data(data_time,class_data_time)
        deal_data(data_place,class_data_place)
        for n in range(0,len(class_data_name)):
            class_list = {'class_name':class_data_name[n],'class_week':class_data_week[n],'class_time':class_data_time[n],'class_place':class_data_place[n]}
            n = n+1
            class_data.append(class_list)
        return class_data

        def deal_time()
            time_data = {'class_name': '新制度经济学', 'class_week': '星期六', 'class_time': '5-6', 'class_place': '会3-101'}
            time_data = time_data['']
x = get_ical('20171016087')

print(x.get_class())