# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/aws.ipynb.

# %% auto 0
__all__ = ['AwsClient']

# %% ../nbs/aws.ipynb 3
import zipfile
import boto3
import tempfile
import shutil
import os

# %% ../nbs/aws.ipynb 4
class AwsClient:
    """
    A client for interacting with AWS services, specifically for operations related to Amazon S3.
    """

    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, region_name: str):
        """
        Initializes the client with AWS credentials and region information.

        Args:
            aws_access_key_id (str): AWS access key ID.
            aws_secret_access_key (str): AWS secret access key.
            region_name (str): AWS region name.
        """
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def upload_to_s3(self, file_path: str, bucket_name: str, object_name: str):
        """
        Uploads a file to an Amazon S3 bucket.

        Args:
            file_path (str): Local path to the file.
            bucket_name (str): Name of the S3 bucket.
            object_name (str): Object name in the S3 bucket (i.e., S3 key).
        """
        self.s3.upload_file(file_path, bucket_name, object_name)

    def extract_zip_with_correct_encoding(self, zip_file_path: str, extract_to_path: str, encoding: str = 'cp437'):
        """
        Extracts a ZIP file with specific encoding for the file names.

        Args:
            zip_file_path (str): Path to the ZIP file.
            extract_to_path (str): Path to extract the ZIP contents to.
            encoding (str, optional): Encoding to use for file names. Defaults to 'cp437'.
        """
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            for member in zip_ref.infolist():
                # ファイル名のエンコーディングを修正
                file_name = member.filename.encode('cp437').decode(encoding)
                target_path = os.path.join(extract_to_path, file_name)
                
                # ディレクトリの場合は作成
                if member.is_dir():
                    os.makedirs(target_path, exist_ok=True)
                else:
                    # ファイルを展開
                    with zip_ref.open(member, 'r') as source, open(target_path, 'wb') as target:
                        shutil.copyfileobj(source, target)

    def upload_to_s3_zip(self, zip_file_path: str, dst_path: str, bucket_name: str):
        """
        Extracts a ZIP file and uploads its contents to an Amazon S3 bucket.

        Args:
            zip_file_path (str): Path to the ZIP file.
            dst_path (str): Destination path in the S3 bucket.
            bucket_name (str): Name of the S3 bucket.
        """

        with tempfile.TemporaryDirectory() as tmpdirname:
            # Extract the ZIP file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdirname)

            # Upload the extracted files to S3
            for root, dirs, files in os.walk(tmpdirname):
                for file in files:
                    local_path = os.path.join(root, file)

                    s3_path = os.path.join(dst_path, os.path.relpath(local_path, tmpdirname)).replace("\\", "/")

                    # Perform the actual upload
                    self.s3.upload_file(local_path, bucket_name, s3_path)