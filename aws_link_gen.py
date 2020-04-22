from dice_gen import s3client
from sys import argv

def transform_url(file_name):
    new_url = s3client.generate_presigned_url('get_object', Params = {'Bucket': 'diceart-media', 'Key': 'media/' + file_name}, ExpiresIn = 100)
    return new_url

if __name__ == '__main__':
    transform_url(argv[1])