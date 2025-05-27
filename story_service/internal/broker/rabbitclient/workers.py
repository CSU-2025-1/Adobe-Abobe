import json
import logging
import aio_pika
from internal.repository.redis_repo import RedisRepo

async def consume_filter_history(channel):
    queue = await channel.declare_queue("filter_story", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                try:
                    payload = json.loads(message.body.decode())
                    user_id = payload.get("user_id")
                    timestamp = payload.get("timestamp")

                    if not user_id or not timestamp:
                        raise ValueError("Missing 'user_id' or 'timestamp' in request")

                    redis = RedisRepo()
                    history = await redis.get_filter_history(user_id)
                    await redis.close()

                    matched_entry = next(
                        (entry for entry in history if entry.get("timestamp") == timestamp),
                        None
                    )

                    if matched_entry is None:
                        response = { "detail": "История с таким timestamp не найдена" }
                    else:
                        response = {
                            "url": matched_entry["url"],
                            "filters": matched_entry["filters"]
                        }

                    await channel.default_exchange.publish(
                        aio_pika.Message(
                            body=json.dumps(response).encode(),
                            correlation_id=message.correlation_id
                        ),
                        routing_key=message.reply_to
                    )
                except Exception as e:
                    logging.warning(f"[story_service] Failed to process message: {e}")