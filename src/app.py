from stats import civitai, liblib, shakker
from apscheduler.triggers.interval import IntervalTrigger
from plombery import  Trigger, register_pipeline


register_pipeline(
    id="Civitai模型统计",
    description="统计Civitai全量flux和sd35模型数量",
    tasks=[civitai.count_civitai_models_task],
    triggers=[
        Trigger(
            id="weekly",
            name="每周",
            description="每周统计一次",
            schedule=IntervalTrigger(weeks=1)
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
            schedule=IntervalTrigger(weeks=1)
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
            schedule=IntervalTrigger(weeks=1)
        )
    ]
)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('plombery:get_app', reload=True, factory=True)