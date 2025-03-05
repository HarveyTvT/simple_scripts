import matplotlib.pyplot as plt
import numpy as np


plt.rcParams['font.family'] = ['Source Han Sans CN']

records = []
country_count = {}
with open('./output.csv', 'r+', encoding='utf-8') as f:
    lines = f.readlines()
    records = [list(x.strip().split(',')) for x in lines]
    for record in records:
        if len(record) != 3:
            continue
        country = record[2]
        if country not in country_count:
            country_count[country] = 0
        country_count[country] += 1
total_cnt = len(records)

data = []
labels = []
pairs = []

for country, cnt in country_count.items():
    pairs.append((country, cnt))

pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

with open('./country_count.csv', 'w+') as f:
    for country, cnt in pairs:
        f.write(f'{country},{cnt}\n')
        f.flush()
        data.append(cnt)
        labels.append(country)

plt.pie(data, labels=labels, autopct='%1.1f%%')
plt.title('IP Distribution')
plt.show()


