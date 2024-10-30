import requests
import json
import time
from prettytable import PrettyTable


def GetModelsCount(types, periodTime):
    current_timestamp = int(time.time() * 1000)

    url = "https://www.liblib.art/api/www/model/feed/stream?timestamp=" + \
        str(current_timestamp)

    payload = json.dumps({
        "isHome": True,
        "cid": "1730236539008ygusxpor",
        "page": 1,
        "pageSize": 30,
        "requestId": "0b79776e-f763-481a-a95e-7867030e5d01",
        "sort": 1,
        "followed": 0,
        "periodTime": [
            periodTime
        ],
        "tagIds": [],
        "models": [],
        "types": types,
        "vipType": [],
        "modelUsage": [],
        "modelLicense": [],
        "tagV2Id": None
    })
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'akhqauth': 'd05abddb3325234dbd07eb59',
        'content-type': 'application/json',
        'cookie': 'acw_tc=0bd17c6617302365389968110e5505ee6b2189366c315d5bc843a5b60e469c; webid=1730236539008ygusxpor; AGL_USER_ID=31a578ac-969f-4b62-847c-41941269eadc; _ga=GA1.1.11076275.1730236541; _bl_uid=6qm2z235ugFy905wavtdkmXo2g8z; _ga_24MVZ5C982=GS1.1.1730236540.1.1.1730236595.5.0.0',
        'origin': 'https://www.liblib.art',
        'priority': 'u=1, i',
        'referer': 'https://www.liblib.art/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'webid': '1730236539008ygusxpor'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if 'data' in response.json() and 'total' in response.json()['data']:
        return response.json()['data']['total']
    else:
        return 0


week_flux_count = GetModelsCount([19], 'week')
week_sd35l_count = GetModelsCount([21], 'week')
week_sd35m_count = GetModelsCount([20], 'week')
week_sd3_count = GetModelsCount([7], 'week')
week_hunyuan_count = GetModelsCount([8, 12], 'week')
week_kolors_count = GetModelsCount([11], 'week')

all_flux_count = GetModelsCount([19], 'all')
all_sd35l_count = GetModelsCount([21], 'all')
all_sd35m_count = GetModelsCount([20], 'all')
all_sd3_count = GetModelsCount([7], 'all')
all_hunyuan_count = GetModelsCount([8, 12], 'all')
all_kolors_count = GetModelsCount([11], 'all')

table = PrettyTable(['BaseModel', 'Week', 'All'], title="LibLib Stats")
table.add_row(['Flux', week_flux_count, all_flux_count])
table.add_row(['SD 3.5 L', week_sd35l_count, all_sd35l_count])
table.add_row(['SD 3.5 M', week_sd35m_count, all_sd35m_count])
table.add_row(['SD 3', week_sd3_count, all_sd3_count])
table.add_row(['Hunyuan', week_hunyuan_count, all_hunyuan_count])
table.add_row(['Kolors', week_kolors_count, all_kolors_count])
print(table)
