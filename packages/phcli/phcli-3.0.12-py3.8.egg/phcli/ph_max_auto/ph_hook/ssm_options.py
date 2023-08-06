import boto3

def get_args_from_ssm(kwargs):
    ssm_client = boto3.client('ssm', region_name='cn-northwest-1')
    response = ssm_client.get_parameter(
        Name='spark_args'
    )
    args = eval(response['Parameter']['Value'])
    return args

def delete_args_from_ssm(kwargs):
    ssm_client = boto3.client('ssm', region_name='cn-northwest-1')
    ssm_client.delete_parameter(
        Name=kwargs.get('job_args_name')
    )

if __name__ == '__main__':
    asd = get_args_from_ssm({1:1})
    print(asd)