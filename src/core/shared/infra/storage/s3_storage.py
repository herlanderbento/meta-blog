from src.core.shared.application.storage_interface import IStorage
from dotenv import load_dotenv

import os
import boto3
from pathlib import Path
import mimetypes

load_dotenv(dotenv_path=os.path.join("envs/.env"))


class S3Storage(IStorage):
    def __init__(self) -> None:

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("R2_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("R2_SECRET_ACCESS_KEY"),
            endpoint_url=f"https://{os.environ.get('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com",
            region_name="auto",
        )
        self.bucket_name = os.environ.get("R2_BUCKET_NAME")

    def store(self, file_path: Path, content: bytes, content_type: str = "") -> str:
        if not content_type:
            content_type, _ = mimetypes.guess_type(str(file_path))

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=str(file_path),
            Body=content,
            ContentType=content_type or "application/octet-stream",
        )

        return f"{os.environ.get('R2_ENDPOINT_URL')}/{self.bucket_name}/{file_path}"

    def get(self, file_path: Path) -> bytes:
        response = self.s3_client.get_object(
            Bucket=self.bucket_name, Key=str(file_path)
        )
        print(f"response {response}")
        return response["Body"].read()

    def delete(self, file_path: Path) -> None:
        list_paths = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
        if "Contents" in list_paths:
            for path in list_paths["Contents"]:
                if str(file_path) in path["Key"]:
                    self.s3_client.delete_object(
                        Bucket=self.bucket_name, Key=path["Key"]
                    )
