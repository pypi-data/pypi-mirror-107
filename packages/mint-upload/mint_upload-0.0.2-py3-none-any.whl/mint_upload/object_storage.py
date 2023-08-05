# -*- coding: utf-8 -*-
"""Class to upload data to the object storage
"""
import json
import logging
from pathlib import Path
import requests
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from mint_upload.progress_percentage import ProgressPercentage


class Uploader:
    """Class to upload data to a object store
    """

    def __init__(self, s3_server: str, auth_server: str, username: str, password: str):
        """Constructor

        Args:
            s3_server (str): S3 server url https://..
            auth_server (str): Auth server url https://
            username (str): The username
            password (str): The password
        """
        self.s3_server = s3_server
        self.auth_server = auth_server
        self.sts_client = boto3.client(
            'sts',
            region_name='us-east-1',
            use_ssl=False,
            endpoint_url=s3_server,
        )
        self.username = username
        self._password = password
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'username': self.username,
            'password': self._password,
            'grant_type': 'password',
            'client_id': 'minio'
        }
        response = requests.post(
            self.auth_server, headers=headers, data=data, allow_redirects=False)
        tokens = json.loads(response.text)
        if response.status_code == 401:
            raise requests.exceptions.HTTPError("401")
        
        if not "access_token" in tokens:
            raise requests.exceptions.HTTPError("500")
     
        access_token = tokens['access_token']

        response = self.sts_client.assume_role_with_web_identity(
            RoleArn='arn:aws:iam::123456789012:user/svc-internal-api',
            RoleSessionName='test',
            WebIdentityToken=access_token,
            DurationSeconds=604800
        )
        self.access_key_id = response['Credentials']['AccessKeyId']
        self.secret_access_key = response['Credentials']['SecretAccessKey']
        session_token = response['Credentials']['SessionToken']
        s3_resource = boto3.resource('s3',
                                     endpoint_url=self.s3_server,
                                     aws_access_key_id=self.access_key_id,
                                     aws_secret_access_key=self.secret_access_key,
                                     aws_session_token=session_token,
                                     config=Config(signature_version='s3v4'),
                                     region_name='us-east-1')
        self.client = s3_resource.meta.client

    def upload_file(self, file_name: str, bucket_name: str, object_name: str = None):
        """Upload a file

        Args:
            file_name (str): File to upload
            bucket_name (str): Bucket to upload to
            object_name (str, optional): S3 object name. If not specified the file_name is used. \
                Defaults to None.

        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = Path(file_name).name

        try:
            self.client.upload_file(
                file_name,
                bucket_name,
                object_name,
                Callback=ProgressPercentage(file_name)
            )
        except ClientError as error:
            raise error
        
    def create_bucket(self, bucket_name: str) -> bool:
        """Create a new bucket

        Args:
            bucket_name (str): The bucket name

        Returns:
            boolean: True if success, false failue
        """
        # Create bucket
        try:
            self.client.create_bucket(Bucket=bucket_name)
        except ClientError as error:
            logging.error(error)
            return False
        return True

    def get_cmd_line(self) -> str:
        """Return the line to configure minio client if the user wants to use cmd

        Returns:
            str: the cmdline
        """
        cmd = f"""mc alias set minio_{self.username} \
            {self.s3_server} {self.access_key_id} {self.secret_access_key} --api S3v4"""
        return cmd
