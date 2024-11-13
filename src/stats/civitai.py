import requests
import json
import urllib.parse
from datetime import datetime, timedelta

from plombery import task, get_logger


# period: Week, Month
# cursor: 2024-10-31T17:24:19.993Z
# base_models: ["Flux.1 D", "Flux.1 S"]
def get_civitai_models(period, cursor, base_models):
    params = {
        "json": {
            "period": period,
            "periodMode": "published",
            "sort": "Newest",
            "types": ["Checkpoint", "TextualInversion", "Hypernetwork", "AestheticGradient", "Upscaler", "Controlnet", "DoRA", "LoCon", "LORA", "MotionModule", "VAE", "Poses", "Wildcards", "Other"],
            "baseModels": base_models,
            "pending": False,
            "browsingLevel": 31,
            "cursor": cursor,
            "authed": True
        }
    }
    params_str = json.dumps(params)
    params_str = urllib.parse.quote_plus(params_str)
    response = requests.get("https://civitai.com/api/trpc/model.getAll?input="+params_str)
    if not response.ok:
        return [], None

    results = []
    cursor = None
    if 'result' in response.json() and 'data' in response.json()['result'] and 'json' in response.json()['result']['data']:
        if 'items' in response.json()['result']['data']['json']:
            results = response.json()['result']['data']['json']['items']
        if 'nextCursor' in response.json()['result']['data']['json']:
            cursor = response.json()['result']['data']['json']['nextCursor']
    return results, cursor


def count_civitai_models(period, base_models):
    cursor = (datetime.now() + timedelta(days=1)
              ).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    total_count = 0
    while True:
        models, cursor = get_civitai_models(period, cursor, base_models)
        total_count += len(models)
        print("new models: ", len(models), "total count: ", total_count)
        if len(models) == 0 or cursor is None:
            break

    return total_count


@task
def count_civitai_models_task():
    logger = get_logger()

    flux_count =  count_civitai_models("AllTime", ["Flux.1 D", "Flux.1 S"])
    logger.info("flux count: %d", flux_count)

    sd35_count = count_civitai_models(
        "AllTime", ["SD 3.5", "SD 3.5 Medium", "SD 3.5 Large", "SD 3.5 Large Turbo"])
    logger.info("sd35 count: %d", sd35_count)

    return [
        {
            'base model': 'Flux',
            'count': flux_count
        },
        {
            'base model': 'SD 3.5',
            'count': sd35_count
        }
    ]
