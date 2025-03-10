import requests
import json
import time
from apscheduler.triggers.interval import IntervalTrigger
from plombery import task, get_logger, Trigger, register_pipeline


def get_shakker_models_count(types):
    current_timestamp = int(time.time() * 1000)

    url = "https://www.shakker.ai/api/www/model/feed/stream?timestamp=" + \
        str(current_timestamp)

    payload = json.dumps({
        "cid": "1730235209237yegdcoul",
        "page": 1,
        "pageSize": 10,
        "sort": 1,
        "followed": "0",
        "periodTime": [
            "all"
        ],
        "tagIds": [],
        "models": [],
        "types": types,
        "vipType": [],
        "modelUsage": [],
        "modelLicense": []
    })
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'akhqauth': 'd05abddb3325234dbd07eb59',
        'content-type': 'application/json',
        'cookie': 'webid=1730235209237yegdcoul; _ga=GA1.1.896594643.1730235211; _bl_uid=p8m122FyuL6xCbddgd55ejOohF6X; _yjsu_yjad=1730235211.c20cf43e-8399-4c00-9ec0-5a29b2d7f1b2; _pin_unauth=dWlkPU9HRXhNemd3TURndE1EQTFNQzAwTTJJNUxUaGhaRFV0TTJOalpEQTNNekUwWm1abA; _rdt_uuid=1730235211312.11d999fd-e552-4448-8b78-d905ba2abdc9; _rdt_em=0000000000000000000000000000000000000000000000000000000000000001; _ga_S0NDCL8GH6=GS1.1.1730235211.1.1.1730235246.25.0.0',
        'origin': 'https://www.shakker.ai',
        'priority': 'u=1, i',
        'referer': 'https://www.shakker.ai/models?from=brand_head_bar',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'webid': '1730235209237yegdcoul',
        'x-language': 'en'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if 'data' in response.json() and 'total' in response.json()['data']:
        return response.json()['data']['total']
    else:
        return 0


@task
def count_shakker_models_task():
    logger = get_logger()

    logger.info("统计Shakker模型数量")
    flux_count = get_shakker_models_count([19])
    sd35l_count = get_shakker_models_count([21])
    sd35m_count = get_shakker_models_count([20])
    pony_count = get_shakker_models_count([10])

    return [
        {
            'base model': 'Flux',
            'count': flux_count
        },
        {
            'base model': 'SD35L',
            'count': sd35l_count
        },
        {
            'base model': 'SD35M',
            'count': sd35m_count
        },
        {
            'base model': 'Pony',
            'count': pony_count
        }
    ]
