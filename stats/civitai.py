import requests
import json
from datetime import datetime
from prettytable import PrettyTable


# period: Week, Month
# cursor: 2024-10-31T17:24:19.993Z
# base_models: ["Flux.1 D", "Flux.1 S"]
def GetModels(period, cursor, base_models):
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
    proxies = {"http": "127.0.0.1:7890"}
    response = requests.get("https://civitai.com/api/v1/models", params=params, proxies=proxies)
    if not response.ok:
        print(params)
        print(response.text)
        return [], None

    results = []
    cursor = None
    if 'items' in response.json():
        results = response.json()['items']
    if 'metadata' in response.json() and 'nextCursor' in response.json()['metadata']:
        cursor = response.json()['metadata']['nextCursor']
    return results, cursor

def count_models(period, base_models):
    cursor = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    total_count = 0
    while True:
        models, cursor = GetModels(period, cursor, base_models)
        total_count += len(models)
        print(f"{base_models}, got {len(models)} models, cursor: {cursor}, total: {total_count}")
        if len(models) == 0 or cursor is None:
            break

    return total_count


flux_count = count_models("AllTime", ["Flux.1 D", "Flux.1 S"])
sd35_count = count_models("AllTime", ["SD 3.5"])
# pony_count = count_models("AllTime", ["Pony"])


table = PrettyTable(['BaseModel',  'All'], title="Civitai Models")
table.add_row(['Flux', flux_count])
table.add_row(['SD 3.5', sd35_count])
# table.add_row(['Pony', pony_count])
print(table)
