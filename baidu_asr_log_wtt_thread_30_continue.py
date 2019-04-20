# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 02:01:09 2018

@author: admin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 18:09:57 2018

@author: Administrator
"""
# 参考：https://www.cnblogs.com/kunixiwa/p/8609843.html
import threading  
import requests
import wave
import os
import json
import base64
import time

#log_filename="./all_out_log_m_thread_%s.txt"%(str(int(time.time())))
log_filename="./all_out_log_m_thread.txt"
#获取地址
baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
#获取tokent
grant_type = "client_credentials"
#API Key
#client_id = "oRtPNnKGdGeBPokpdQpGnXPN"
client_id = "DugZt412RfX1ZloH39eIs9i7"
#Secret Key
#client_secret = "hVj2f4aGfX0SbqOVrupHGUafIqECQ23G" 
client_secret = "62e0d6c023b7bf0b01c87d22b797a062"
#拼url
url ="%sgrant_type=%s&client_id=%s&client_secret=%s"%(baidu_server,grant_type,client_id,client_secret)
#print(url)
#获取token
response=requests.get(url)
#print(res.text)
res = json.loads(response.content.decode('utf-8'))
token=res['access_token']
#print(token)
#24.b891f76f5d48c0b9587f72e43b726817.2592000.1524124117.282335-10958516

#class MyEncoder(json.JSONEncoder):
#    def default(self, obj):
#        if isinstance(obj, bytes):
#            #return str(obj, encoding='utf-8');
#            return  obj.__str__()
#        return json.JSONEncoder.default(self, obj)
#设置格式
RATE = "16000"
FORMAT = "wav"
CUID="10981989"
DEV_PID=1536
def get_asr(FILENAME):
    result=''
    max_retry_times = 3
    retry=0
    with open(FILENAME, "rb") as f:
        speech = base64.b64encode(f.read()).decode("utf8")
        
    size = os.path.getsize(FILENAME)
    headers = { 'Content-Type' : 'application/json'} 
    url = "https://vop.baidu.com/server_api"
    data={
    
            "format":FORMAT,
            "rate":RATE,
            "dev_pid":DEV_PID,
            "speech":speech,
            "cuid":CUID,
            "len":size,
            "channel":1,
            "token":token,
        }
    if not FILENAME.split('./all_out/')[1] in already_file_list:
        try:
            req = requests.post(url,json.dumps(data),headers)
            result = json.loads(req.text)
        except:
            if 'speech quality error' in result:
                pass
            else:
                while retry < max_retry_times:
                    retry += 1
                    try:
                        req = requests.post(url,json.dumps(data),headers)
                        result = json.loads(req.text)
                        print('tried again:%s'%FILENAME)
                    except:
                        print('retry failed %d,filename=%s'%(retry,FILENAME))
    with open(log_filename,"a", encoding="utf8") as log_file:
        log_file.write("filename=%s ###### result=%s\n"%(FILENAME,result))
#    print(result)




base_dir='./all_out'
thread_num= 3
threads=[]
count=0



already_file_list=[]
with open(log_filename,"r",encoding="utf8") as a_file:
    for line in a_file:
        if '\'result\': [' in line:
            already_file_list.append(line.split('filename=./all_out/')[1].split(' ######')[0])

if 1:#with open("./all_out_log_m_thread.txt","r", encoding="utf8") as log_file:
    for path,pathname,filenames in os.walk(base_dir):
        for filename in filenames:
            if filename.endswith('.wav'):
                count+=1
                if 1:
                    t=threading.Thread(target=get_asr,args=(os.path.join(path,filename),))                         
                    threads.append(t)

kk =0
for t in threads:
    t.start()
    while True:
        if(len(threading.enumerate()) < thread_num):  
            kk+=1
            print(kk)
            break
