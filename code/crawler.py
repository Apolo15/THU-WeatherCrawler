import requests
from bs4 import BeautifulSoup
import chardet
import json as js
import re
import time
import pandas as pd
import pymysql

def crawler(url, header, province, city, district, database, info_table, mydb):
    try:
        i = 0
        while (i < 3):
            try:
                r = requests.get(url, headers=header, timeout=100, verify=True, allow_redirects=True)
                break
            except requests.exceptions.RequestException as e:
                print(e)
                i += 1
        r.encoding = chardet.detect(r.content)['encoding']
        soup = BeautifulSoup(r.text, 'lxml')

        ## 获取sunrise和sunset
        sunTime = soup.find("div", class_="sunTimes")
        sunRise = sunTime.select("span.sunrise.swip > span.time")[0].text.strip()
        sunSet = sunTime.select("span.sunset.swap > span.time")[0].text.strip()

        ## 获取script
        script = soup.select("body.day > script")[0].text
        m = re.search('var hours = (.+)[,;]{1}', script)
        if m:
            found = m.group(1)
        json =js.loads(found)
        # print(type(found))

        # 取中午十二点 
        data = json[12] # type:'dict'
        b = data["time"] if "time" in data else None
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(b)) #time

        appTemp = data["apparentTemperature"] if "apparentTemperature" in data else None #apparentTemperature
        pressure = data["pressure"] if "pressure" in data else None#pressure
        cloudCover = data["cloudCover"] if "cloudCover" in data else None#cloudCover
        dewPoint = data["dewPoint"] if "dewPoint" in data else None#dewPoint
        humidity = data["humidity"] if "humidity" in data else None#humidity
        precipProbability = data["precipProbability"] if "precipProbability" in data else None#preciRate
        #moonPhase
        #nearestStormDis
        #nearestStormDir
        ozone = data["ozone"] if "ozone" in data else None#ozone
        precipType = data["precipType"] if "precipType" in data else None#preciType
        precipAccumulation = data["precipAccumulation"] if "precipAccumulation" in data else None#snowFall
        temperature = data["temperature"] if "temperature" in data else None#temperature
        textSummary = data["summary"] if "summary" in data else None#textSummary
        UVIndex = data["uvIndex"] if "uvIndex" in data else None#UVIndex
        windGust = data["windGust"] if "windGust" in data else None#windGust
        windSpeed = data["windSpeed"] if "windSpeed" in data else None#windSpeed
        windBearing = data["windBearing"] if "windBearing" in data else None#windBearing
        precipProbability = data["precipProbability"] if "precipProbability" in data else None#preciRate
        # print(date, province, city, district, appTemp, pressure, cloudCover, dewPoint, humidity, precipProbability, ozone, precipType, precipAccumulation,
        # temperature, textSummary, UVIndex, windGust, sunRise, windSpeed, sunSet, windBearing, lat, long)
        # print(date,data["temperature"])
        # js_test=js.loads(bs.find("script",{"id":"DATA_INFO"}).get_text())
    except:
        print(e)
        return
    else:
        print("爬取成功, 开始插入数据!")
        try:
            # 数据未插入，待确认
            sql = '''select count(*) from ''' + database + '''.''' + info_table + ";"
           
            mydb.ping(reconnect=True)
            cur = mydb.cursor()
            cur.execute(sql)
            num=cur.fetchall()
            print(num)
            mydb.commit()

        except Exception as e:
            print("数据库写入error：", e)
            return
        else:
            print("数据库写入成功！", date, "[", province, city, district,"]")



if __name__ == "__main__":
    header = {
                'method': 'GET',
                'scheme': 'https',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'cache-control': 'max-age=0',
                'cookie': '__gads = ID = a8621179bd19f41b:T = 1622512981:S = ALNI_MZ8LdJWvuZ1Itjo3E0pCUXms78Fow;_gid = GA1.2.1459346967.1622863299;ga_07ZGQT7GK0 = GS1.1.1622863299.2.1.1622863311.0;_ga = GA1.2.1189824484.1622512972',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
                'sec-ch-ua-mobile': '?0',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 91.0.4472.77 Safari / 537.36'
            }
    config={
            'host':'127.0.0.1',
            'user':'root',
            'password':'',
            'autocommit':'True',}
    
    database='weatherdata'
    info_table='gpsinfo'
    mydb=pymysql.connect(**config)
    df=pd.read_excel("gpsInfo.xlsx",sheet_name='gpsinfo')
    # print(df)
    for i in range(df.shape[0]):
        data = df.iloc[i].to_list()
        id, province, city, district, lat, long = data
        t = time.mktime(time.strptime("2010-01-01", '%Y-%m-%d'))
        t_end = time.mktime(time.strptime("2021-10-01", '%Y-%m-%d'))
        while t < t_end:
            date = time.strftime("%Y-%m-%d", time.localtime(t))
            url = "https://darksky.net/details/"+str(lat)+","+str(long)+"/"+date+"/si12/en"
            crawler(url, header, province, city, district, database, info_table, mydb)
            t += 24*60*60 #一天
            time.sleep(10)
    mydb.close()