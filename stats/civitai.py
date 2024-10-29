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
        "token": "58f763daff342bdb95f67299aabc4753",
        "baseModels": base_models
    }

    response = requests.get("https://civitai.com/api/v1/models", params=params)
    if not response.ok:
        print(response.text)
        return [], None

    if 'items' in response.json():
        results = response.json()['items']
        if len(results) == 0:
            return [], None
        return results, response.json()['metadata']['nextCursor']
    else:
        return [], None


def count_models(period, base_models):
    cursor = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    total_count = 0
    while True:
        models, cursor = GetModels(period, cursor, base_models)
        if len(models) == 0:
            break
        total_count += len(models)
    return total_count


flux_count = count_models("AllTime", ["Flux.1 D", "Flux.1 S"])
sd35_count = count_models("AllTime", ["SD 3.5"])
pony_count = count_models("AllTime", ["Pony"])


table = PrettyTable(['BaseModel',  'All'])
table.add_row(['Flux', flux_count])
table.add_row(['SD 3.5', sd35_count])
table.add_row(['Pony', pony_count])
print(table)
