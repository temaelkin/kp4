import boto3

ACCESS_KEY = "ВАШ_ИДЕНТИФИКАТОР_КЛЮЧА"
SECRET_KEY = "ВАШ_СЕКРЕТНЫЙ_КЛЮЧ"

s3 = boto3.client(
    "s3",
    endpoint_url="https://storage.yandexcloud.net",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name="ru-central1",
)
