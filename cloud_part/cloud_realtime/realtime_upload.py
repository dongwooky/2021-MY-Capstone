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
local_file_path = './input_image/input.png'

capture = cv2.VideoCapture(0)

if not capture.isOpened():
    print('Camera open failed!')
    sys.exit()
    
while True:
    ret, frame = capture.read() 
    if not ret:
        print('Frame read error!')
        sys.exit()
    cv2.imshow('Frame', frame)
    cv2.imwrite('./input_image/input.png', frame)
    s3.upload_file(local_file_path, bucket_name, object_name)
    if cv2.waitKey(33) == ord('q'):
        break
capture.release()
cv2.destroyAllWindows()