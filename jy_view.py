import sqlite3
import json
from random import *
from collections import deque
from datetime import datetime

from django.shortcuts import render
from django.utils import timezone
# 모델 가져오기
from .models import Sleep_Data
# HTTP response
from django.http import HttpResponse

# 데이터베이스에서 데이터를 가져와 그래프 페이지를 띄워준다
def show_graph(request):
    # sqlite db 읽어와서 출력
    db_dir = "/home/mhealth/바탕화면/CBP_SLEEP_TEST/tcp_new/sleep/db/"
    conn = sqlite3.connect(db_dir + 'sleep_data.db')
    print ("Opened database successfully")
    # 데이터 읽어오는 select 쿼리문
    select_cmd = "SELECT Name, time, ch1, ch2, realtime from SLEEP_DATA"
    cursor = conn.execute(select_cmd)
    # rows 에는 django template 에서 사용할 그래프 데이터가 저장
    # rows = []
    ch1 = []
    ch2 = []
    for row in cursor:
        # django template 에서 읽기 쉽도록 dictionary 형태로 저장
        # 주의 : django template 은 for loop counter 를 통한 array index 접근을 하기 불편하다
        # print(row)
        # tmp = dict()
        # ch1 과 ch2 를 dict 에 저장한다
        now = datetime.now()
        curr_time = str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second)
        ch1.append([int(curr_time), int(row[2], 16)])
        ch2.append([int(curr_time), int(row[3], 16)])

        # tmp.update({"ch1":row[2]})
        # tmp.update({"ch2":row[3]})
    # rows.append(tmp)
    print ("Operation done successfully")
    for elem in ch1:
        print (elem)
    for elem in ch2:
        print (elem)
    conn.close()
    # return render(request, 'graph/show_graph.html', {'data' : rows})
    return render(request, 'graph/juyeon.html', {'data1' : ch1, 'data2' : ch2})

def get_realtime_data(request):
    db_dir = "/home/mhealth/바탕화면/CBP_SLEEP_TEST/tcp_new/sleep/db/"
    conn = sqlite3.connect(db_dir + 'sleep_data.db')
    select_cmd = "SELECT Name, time, ch1, ch2, realtime FROM SLEEP_DATA ORDER BY realtime DESC LIMIT 1"
    cursor = conn.execute(select_cmd)
    contens = {}

    for row in cursor:
        now = datetime.now()
        curr_time = str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second)
        ch1 = [int(curr_time), int(row[2], 16)]
        ch2 = [int(curr_time), int(row[3], 16)]
        contents = {'data1': ch1, 'data2': ch2}
        print (ch1 + " / " + ch2)
    conn.close()

    return HttpResponse(json.dumps(contents), content_type="application/json")

# 데이터를 저장하는 과정을 거친다
# 앞으로 사용할 일은 없을듯
def store_data(request):
    names = []
    data = []
    # 샘플 데이터를  id(nameX) 에 의해서 읽어온다 / GET 방식, id 일치시켜야함
    names.append(request.GET.get('name1', 'noname'))
    data.append(request.GET.get('ex_data1', ''))

    for i, d in enumerate(data):
        hex_components = []
        # underscore(_) 에 의해서 파싱한다
        hex_components = d.split('_')
        decimal_components = []
        # underscore 로 구분된 데이터 조각 하나를 16진수에서 10진수로 변환한다
        for c in hex_components:
            # 16진수 표시를 한다
            hex_c = "0x" + c
            # 16진수를 10진수로 변환한다
            decimal_components.append(int(hex_c, 16))
            Sleep_Data.objects.create(name=names[i], data_a=decimal_components[0], data_b= decimal_components[1], data_c= decimal_components[2], data_d= decimal_components[3], data_e= decimal_components[4], data_f=decimal_components[5])
            sleep_data = Sleep_Data.objects.get(name=names[i])
            sleep_data.publish()

    return HttpResponse('데이터가 성공적으로 저장되었습니다')

# example data 를 전송하는 페이지를 띄워준다
def show_new_graph(request):
    return render(request, 'graph/new_graph.html')

def get_cbp_data(request):
    print(request.GET.get('a'))
    return  HttpResponse("I m here")


real_time_ch1_buffer = deque()
real_time_ch2_buffer = deque()

def set_data(request):
    real_time_ch1_buffer.append(int(request.GET['real_time_data1']))
    print(request.GET['real_time_data1'])
    real_time_ch2_buffer.append(int(request.GET['real_time_data2']))
    print(request.GET['real_time_data2'])
    return HttpResponse("ok")

def get_data(request):
    response_data = {}
    if real_time_ch1_buffer and real_time_ch2_buffer:
        response_data['new_data1'] = real_time_ch1_buffer.popleft()
        response_data['new_data2'] = real_time_ch2_buffer.popleft()
    else :
        response_data['new_data1'] = ""
        response_data['new_data2'] = ""
    response_data['result'] = 'error'
    response_data['message'] = 'Some error message'
    return HttpResponse(json.dumps(response_data), content_type="application/json")
