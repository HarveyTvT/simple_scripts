import requests
from datetime import datetime

from plombery import task, get_logger


# period: Week, Month
# cursor: 2024-10-31T17:24:19.993Z
# base_models: ["Flux.1 D", "Flux.1 S"]
def get_civitai_models(period, cursor, base_models):
    params = {
        "limit": 100,
        "cursor": cursor,
        "types": [
            "Checkpoint",
            "TextualInversion",
            "Hypernetwork",
            "AestheticGradient",
            "Upscaler",
            "MotionModule",
            "Other",
            "Controlnet",
            "DoRA",
            "Wildcards",
            "LoCon",
            "Poses",
            "VAE",
            "LORA"
        ],
        "sort": "Newest",
        "period": period,
        "periodMode": "published",
        "token": "58f763daff342bdb95f67299aabc4753",
        "baseModels": base_models
    }
    response = requests.get("https://civitai.com/api/v1/models", params=params)
    if not response.ok:
        return [], None

    results = []
    cursor = None
    if 'items' in response.json():
        results = response.json()['items']
    if 'metadata' in response.json() and 'nextCursor' in response.json()['metadata']:
        cursor = response.json()['metadata']['nextCursor']
    return results, cursor


def count_civitai_models(period, base_models):
    cursor = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    total_count = 0
    while True:
        models, cursor = get_civitai_models(period, cursor, base_models)
        total_count += len(models)
        if len(models) == 0 or cursor is None:
            break

    return total_count


@task
def count_civitai_models_task():
    flux_count =  count_civitai_models("AllTime", ["Flux.1 D", "Flux.1 S"])
    sd35_count = count_civitai_models("AllTime", ["SD 3.5"])
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
