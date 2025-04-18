from api.filter import filter_pb2_grpc, filter_pb2
from internal.core.usecase.apply_filter_usecase import apply_filter_usecase
from internal.repository.redis_repo import RedisRepo
from internal.repository.s3_repo import S3Repo


class FilterServiceServicer(filter_pb2_grpc.FilterServiceServicer):
    async def ApplyFilters(self, request, context):
        image_id = request.image_id
        filters = dict(request.filters)

        redis_repo = RedisRepo()
        s3_repo = S3Repo()

        filtered_url = await apply_filter_usecase(
            image_id=image_id,
            filters=filters,
            redis_repo=redis_repo,
            s3_repo=s3_repo
        )

        return filter_pb2.FilterResponse(filtered_url=filtered_url)
