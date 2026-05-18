from minio import Minio

from xybook_common.config import ServiceSettings

BUCKETS = ["xybook-avatars", "xybook-media", "xybook-exports"]


def get_minio_client(
    endpoint: str, access_key: str, secret_key: str, secure: bool = False
) -> Minio:
    return Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)


def ensure_buckets(client: Minio) -> None:
    for bucket in BUCKETS:
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
