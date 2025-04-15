from stats import civitai, liblib, shakker
from stats.civitai import InputParams, GetCreatorModelsParams
from apscheduler.triggers.interval import CronTrigger
from plombery import  Trigger, register_pipeline


register_pipeline(
    id="Civitai模型统计",
    description="Civitai模型统计",
    tasks=[civitai.count_civitai_models_task],
    triggers=[
        Trigger(
            id="weekly",
            name="每周",
            description="每周统计一次",
            schedule=CronTrigger(day_of_week=2,hour=12)
        )
    ]
)

register_pipeline(
    id="Liblib模型统计",
    description="Liblib模型统计",
    tasks=[liblib.count_liblib_models_task],
    triggers=[
        Trigger(
            id="weekly",
            name="每周",
            description="每周统计一次",
            schedule=CronTrigger(day_of_week=2,hour=12)
        )
    ]
)

register_pipeline(
    id="Shakker模型统计",
    description="Shakker模型统计",
    tasks=[shakker.count_shakker_models_task],
    triggers=[
        Trigger(
            id="weekly",
            name="每周",
            description="每周统计一次",
            schedule=CronTrigger(day_of_week=2,hour=12)
        )
    ]
)


register_pipeline(
    id="civitai排行榜统计",
    description="参数直接贴civitai排行榜链接，比如: https://civitai.com/leaderboard/flux?board=legend",
    tasks=[civitai.get_civitai_leaderboard_task],
    params=InputParams
)

register_pipeline(
    id="civitai获取用户所有模型链接",
    description="参数直接贴c站用户id，比如: Void91",
    tasks=[civitai.get_creator_models],
    params=GetCreatorModelsParams
)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('plombery:get_app', reload=True, factory=True, host='0.0.0.0', port=8000)
