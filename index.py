import holidays
import json

holidays.getYearHolidays('2021')

with open('data.json','r')as fp:
    json_data = json.load(fp)

f = open('openday.sql', 'w',encoding='utf-8')
for month in json_data:
    #for day in days[month]:
    for (k,v) in  json_data[month].items():
        #print ('======key========:'+str(k)+"************value******"+str(v))
        if v==1:
           sql = "insert into TOPENDAY (D_DATE, L_WORKFLAG, C_MEMO)values (to_date('%s', 'yyyymmdd'), 1, '工作日');" %k 
           #print("insert into TOPENDAY (D_DATE, L_WORKFLAG, C_MEMO)values (to_date('%s', 'yyyymmdd'), 1, '工作日');" % k)
        else:
           #print("insert into TOPENDAY (D_DATE, L_WORKFLAG, C_MEMO)values (to_date('%s', 'yyyymmdd'), 0, '非工作日');" % k)
           sql = "insert into TOPENDAY (D_DATE, L_WORKFLAG, C_MEMO)values (to_date('%s', 'yyyymmdd'), 0, '非工作日');" %k 
        f.write(sql)
        f.write('\n')
 # 文件写入内容
f.close()
#print(days);