import logging
import boto3
from dogemachine_utils.time import get_year_month_day_string, get_current_time_string
from dogemachine_utils.files import read_file
from dogemachine_utils.aws_lambda import is_running_in_aws_lambda, is_running_in_sam_cli_local
from dogemachine_utils.aws_login import get_boto3_client, get_current_account_id
logger = logging.getLogger(__name__)


def get_doge_machine_bucket_name() -> str:
    """Get the standard name of the Doge Machine bucket"""
    account_id = get_current_account_id()
    name = f"doge-machine-results-{account_id}"
    return name


def get_object_from_s3(bucket_name: str, object_key: str, s3_client: boto3.Session.client):
    """Get object contents from  S3"""
    logger.info(f"Downloading object: s3://{bucket_name}/{object_key}")
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    content = response['Body'].read().decode('utf-8')
    return content


def write_simple_object_to_s3(content: str, bucket_name: str, object_key: str, s3_client: boto3.Session.client):
    """Write an object to S3 with basic AES256 encryption"""
    logger.info(f"Writing object: s3://{bucket_name}/{object_key}")
    response = s3_client.put_object(
        ACL="private",
        Bucket=bucket_name,
        Key=object_key,
        ServerSideEncryption="AES256",
        Body=content
    )
    logger.debug(response)


def save_results_file_to_s3_from_aws_lambda(
        target_url: str,
        tool_name: str,
        results_file: str,
        bucket: str,
):
    """
    If it's running in AWS Lambda, save the file contents to S3

    :param bucket:
    :param target_url:
    :param tool_name:
    :param results_file:
    :return:
    """
    contents = read_file(results_file)
    print(contents)
    if not is_running_in_sam_cli_local() and is_running_in_aws_lambda():
        print("Saving to S3...")
        s3_client = get_boto3_client(service="s3", region="us-east-1", profile=None)
        # TODO: Change the region detection here?
        write_simple_object_to_s3(
            content=contents,
            bucket_name=bucket,
            object_key=f"{target_url}/{tool_name}/{get_year_month_day_string()}/{get_current_time_string()}-results.xml",
            s3_client=s3_client
        )
