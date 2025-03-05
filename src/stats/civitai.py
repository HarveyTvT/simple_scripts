import requests
import json
import time
import urllib.parse
from datetime import datetime, timedelta

from plombery import task, get_logger, BaseModel

# --------------------------------------------------------------------------------


class CivitaiApi:
    def call_trpc(self, method, params):
        params_str = json.dumps(params)
        params_str = urllib.parse.quote_plus(params_str)

        headers = {
            "content-type": "application/json",
            "referer": "https://civitai.com/",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-platform': "Linux",
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'X-Client': 'web',
            'x-client-date': str(round(time.time() * 1000)),
            'x-client-version': '5.0.249',
            'x-fingerprint': 'c6cb00d14274be85fbb3f649d3b48d3eca049cbdf12344c731b4b572e98511e19a8a5e9cbad0beb59de6602bb2cc44a1'
        }
        response = requests.get(
            f"https://civitai.com/api/trpc/{method}?input={params_str}", headers=headers)
        if not response.ok:
            print(response.text)
            print(response.status_code)
            return None
        if 'result' in response.json() and 'data' in response.json()['result'] and 'json' in response.json()['result']['data']:
            return response.json()['result']['data']['json']
        return None

    # period: Week, Month
    # cursor: 2024-10-31T17:24:19.993Z
    # base_models: ["Flux.1 D", "Flux.1 S"]
    def get_models(self, period: str, cursor: str, base_models: list[str], username: str = ''):
        params = {
            "json": {
                "period": period,
                "periodMode": "published",
                "sort": "Newest",
                "types": ["Checkpoint", "TextualInversion", "Hypernetwork", "AestheticGradient", "Upscaler", "Controlnet", "DoRA", "LoCon", "LORA", "MotionModule", "VAE", "Poses", "Wildcards", "Other"],
                "pending": False,
                "browsingLevel": 31,
                "cursor": cursor,
                "authed": True
            }
        }
        if base_models is not None and len(base_models) > 0:
            params["json"]["baseModels"] = base_models
        if username != '':
            params["json"]["username"] = username

        respData = self.call_trpc("model.getAll", params)
        if respData is None:
            return [], None
        if 'items' in respData:
            results = respData['items']
        if 'nextCursor' in respData:
            cursor = respData['nextCursor']
        return results, cursor

    # --------------------------------------------------------------------------------
    # 新创作者榜：https://civitai.com/leaderboard/new_creators  , new_creators
    # 仅90天创作者排行榜：https://civitai.com/leaderboard/overall_90, overall_90
    # Flux排行榜：https://civitai.com/leaderboard/flux,  flux
    # SDXL排行榜：https://civitai.com/leaderboard/sdxl, sdxl
    # Pony排行榜：https://civitai.com/leaderboard/pony, pony
    def get_leaderboard_users(self, board_id: str, is_legend: bool):
        params = {
            "json": {
                "id": board_id,
                "authed": True,
            }
        }

        method = "leaderboard.getLeaderboard"
        if is_legend:
            method = "leaderboard.getLeadboardLegends"

        items = self.call_trpc(method, params)
        if items is None:
            return []

        return list({'rank': f"{board_id}#{idx}", 'userid': i['user']['id'], 'username': i['user']['username'], 'score': i['score']} for idx, i in enumerate(items) if 'user' in i)

    def get_creator(self, username: str):
        params = {
            "json": {
                "username": username,
                "authed": True
            }
        }
        return self.call_trpc("user.getCreator", params)


def count_civitai_models(period, base_models):
    civitaiapi = CivitaiApi()
    cursor = (datetime.now() + timedelta(days=1)
              ).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    total_count = 0
    while True:
        models, cursor = civitaiapi.get_models(period, cursor, base_models)
        total_count += len(models)
        print("new models: ", len(models), "total count: ", total_count)
        if len(models) == 0 or cursor is None:
            break
        time.sleep(0.5)
    return total_count


@task
def count_civitai_models_task():
    logger = get_logger()

    illustrious_count = count_civitai_models("AllTime", ["Illustrious"])
    logger.info(f"Illustrious count: {illustrious_count}")

    sd35_count = count_civitai_models(
        "AllTime", ["SD 3.5", "SD 3.5 Medium", "SD 3.5 Large", "SD 3.5 Large Turbo"])
    logger.info(f"SD 3.5 count: {sd35_count}")

    flux_count = count_civitai_models("AllTime", ["Flux.1 D", "Flux.1 S"])
    logger.info(f"Flux count: {flux_count}")

    return [
        {
            'base model': 'Flux',
            'count': flux_count
        },
        {
            'base model': 'SD 3.5',
            'count': sd35_count
        },
        {
            'base model': 'Illustrious',
            'count': illustrious_count
        }
    ]


class InputParams(BaseModel):
    board_url: str  # https://civitai.com/leaderboard/sdxl


@task
def get_civitai_leaderboard_task(params: InputParams):
    parsed_url = urllib.parse.urlparse(params.board_url)
    board = parsed_url.path.split('/')[-1]
    is_legend = parsed_url.query == "board=legend"

    civitaiapi = CivitaiApi()
    results = civitaiapi.get_leaderboard_users(board, is_legend)

    for creator in results:
        creator_info = civitaiapi.get_creator(creator['username'])
        if creator_info is None:
            continue
        if 'links' in creator_info:
            creator['links'] = '\n'.join(
                list(x['url'] for x in creator_info['links']))
        if 'stats' in creator_info:
            creator['download_count'] = creator_info['stats']['downloadCountAllTime'] if 'downloadCountAllTime' in creator_info['stats'] else 0
            creator['favorite_count'] = creator_info['stats']['favoriteCountAllTime'] if 'favoriteCountAllTime' in creator_info['stats'] else 0
            creator['thumbsup_count'] = creator_info['stats']['thumbsUpCountAllTime'] if 'thumbsUpCountAllTime' in creator_info['stats'] else 0
            creator['follower_count'] = creator_info['stats']['followerCountAllTime'] if 'followerCountAllTime' in creator_info['stats'] else 0
            creator['generation_count'] = creator_info['stats']['generationCountAllTime'] if 'generationCountAllTime' in creator_info['stats'] else 0
        if '_count' in creator_info:
            creator['model_count'] = creator_info['_count']['models'] if 'models' in creator_info['_count'] else 0
        time.sleep(0.1)

    return results


class GetCreatorModelsParams(BaseModel):
    username: str  # Void91


@task
def get_creator_models(params: GetCreatorModelsParams):
    username = params.username

    civitaiapi = CivitaiApi()
    cursor = (datetime.now() + timedelta(days=1)
              ).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    total_count = 0
    model_urls = []

    while True:
        models, cursor = civitaiapi.get_models("AllTime", cursor, [], username)
        total_count += len(models)
        for m in models:
            model_urls.append({
                "url": f"https://civitai.com/models/{m['id']}/{m['name']}"
            })
        print("models: ", len(models), "total count: ", total_count)
        if len(models) == 0 or cursor is None:
            break
        time.sleep(0.5)
    return model_urls
