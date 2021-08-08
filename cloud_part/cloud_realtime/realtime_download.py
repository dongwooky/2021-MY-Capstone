import cv2
import sys
import boto3

service_name = 's3'
endpoint_url = 'https://kr.object.ncloudstorage.com'
region_name = 'kr-standard'
accesss_key = 'OTOSP4zl6AHejEc10Bj7'
secret_key = 'FNzp5yHsjUgIGa2Uk9uTTZTRUZ4bGAPEWxhtjtiL'

s3= boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=accesss_key,
                     aws_secret_access_key=secret_key)

bucket_name = 'dwkrefrigerator'
    
object_name = 'refrigerator_image'
local_file_path = './input_image/output.png'

while True:
    s3.download_file(bucket_name, object_name, local_file_path)
    frame = cv2.imread('./input_image/output.png')
    cv2.imshow('frame', frame)
    if cv2.waitKey(33) == ord('q'):
        break
cv2.destroyAllWindows()    