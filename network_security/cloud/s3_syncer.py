import os


class S3Sync:
    def sync_folder_to_s3(self, folder: str, aws_bucket_url: str) -> None:
        command = f"aws s3 sync {folder} {aws_bucket_url} "
        os.system(command)

    def sync_folder_from_s3(self, folder: str, aws_bucket_url: str) -> None:
        command = f"aws s3 sync  {aws_bucket_url} {folder} "
        os.system(command)
