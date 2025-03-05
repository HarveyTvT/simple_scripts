import maxminddb

records = []
with open('./input.csv', 'r+') as f:
    lines = f.readlines()
    records = [list(x.strip().split(',')) for x in lines][1:]

null_count = 0
with open('./output.csv', 'w+') as f:
    with maxminddb.open_database('GeoLite2-City.mmdb') as reader:
        i = 0
        for record in records:
            ip = record[1]

            resp = reader.get(ip)
            print(resp)

            if resp is None:
                null_count += 1
                continue
            if 'country' not in resp:
                continue
            if 'names' not in resp['country']:
                continue
            if 'zh-CN' not in resp['country']['names']:
                continue

            record.append(resp['country']['names']['zh-CN'])
            line = ','.join(record) + '\n'
            print(line)
            f.write(line)

            i += 1
            if i % 10 == 0:
                f.flush()

print("null count: ", null_count)
