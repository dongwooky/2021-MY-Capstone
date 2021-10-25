import boto3

service_name = 's3'
endpoint_url = 'https://kr.object.ncloudstorage.com'
region_name = 'kr-standard'
accesss_key = 'OTOSP4zl6AHejEc10Bj7'
secret_key = 'FNzp5yHsjUgIGa2Uk9uTTZTRUZ4bGAPEWxhtjtiL'

if __name__ == "__main__":
    s3= boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=accesss_key,
                     aws_secret_access_key=secret_key)
    
    bucket_name = 'dwkrefrigerator'
    
    object_name = 'fridge_list'
    local_file_path = './hi.txt'
    
    s3.upload_file(local_file_path, bucket_name, object_name)