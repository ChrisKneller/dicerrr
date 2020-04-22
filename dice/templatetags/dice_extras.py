from django import template
import boto3
import os

register = template.Library()

@register.simple_tag
def static_aws(url):
    session = boto3.session.Session(region_name='eu-west-2',aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", ""),aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", ""))
    s3client = session.client('s3')
    new_url = s3client.generate_presigned_url('get_object', Params = {'Bucket': 'diceart-static', 'Key': 'static/' + url}, ExpiresIn = 100)
    return new_url