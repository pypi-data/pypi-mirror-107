import boto3

def get_args_from_ssm(kwargs):
    ssm_client = boto3.client('ssm')
    response = ssm_client.get_parameter(
        Name=kwargs.get('job_args_name')
    )
    args = eval(response['Parameter']['Value'])
    return args

def delete_args_from_ssm(kwargs):
    ssm_client = boto3.client('ssm')
    ssm_client.delete_parameter(
        Name=kwargs.get('job_args_name')
    )