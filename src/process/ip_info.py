import requests
import json


# 恢复数据，避免重复请求
results = {}
with open('./output.csv', 'r+') as f:
    lines = f.readlines()
    records = [list(x.strip().split(',')) for x in lines][1:]
    for record in records:
        ip = record[2]
        if len(record) != 6:
            continue
        results[ip] = {
            'city': record[3],
            'region': record[4],
            'country': record[5]
        }

records = []
with open('./input.csv', 'r+') as f:
    lines = f.readlines()
    records = [list(x.strip().split(',')) for x in lines][1:]

with open('./output.csv', 'w+') as f:
    i = 0
    for record in records:
        ip = record[2]
        if ip not in results:
            resp = requests.get('https://ipinfo.io/' + record[2] + "?token=91b7d9d74e2216")
            ipinfo = json.loads(resp.text)
            results[ip] = ipinfo
            print(ipinfo)
        ipinfo = results[ip]
        if 'city' in ipinfo:
            record.append(ipinfo['city'])
        if 'region' in ipinfo:
            record.append(ipinfo['region'])
        if 'country' in ipinfo:
            record.append(ipinfo['country'])
        line = ','.join(record) + '\n'
        f.write(line)

        i += 1
        if i % 10 == 0:
            f.flush()



