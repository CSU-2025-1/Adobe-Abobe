from internal.repository.redis_repo import RedisRepo


async def get_filtered_usecase(task_id: str, redis_repo: RedisRepo) -> dict:
    result = await redis_repo.get_filter_result(task_id)

    if result:
        return result
    else:
        return {"status": "processing"}
