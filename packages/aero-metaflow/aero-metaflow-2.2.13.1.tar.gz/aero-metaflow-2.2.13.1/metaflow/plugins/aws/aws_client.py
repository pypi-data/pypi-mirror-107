# File modified under the Apache Licence 2.0 spec. Modified by Aero Technologies.
# Altered how profile is set based on local/remote execution

import os
import configparser

from pathlib import Path

def get_aws_client(module, with_error=False, params={}):
    from metaflow.exception import MetaflowException
    import requests

    user_home = str(Path.home())
    config = configparser.ConfigParser()

    # # Handle case of AWS Batch - no credentials file
    # try:
    #     with open(f"{user_home}/.aws/credentials") as f:
    #         config.read_file(f)

    #     if 'aero' not in config:
    #         raise Exception("Credentials aren't set. Make sure you run 'aero account login' first.")

    #     os.environ['AWS_PROFILE'] = 'aero'

    # except IOError:
    #     print("Error ocurred reading creds")
    #     pass


    try:
        import boto3
        from botocore.exceptions import ClientError
    except (NameError, ImportError):
        raise MetaflowException(
            "Could not import module 'boto3'. Install boto3 first.")

    if with_error:
        return boto3.client(module, **params), ClientError
    return boto3.client(module, **params)
