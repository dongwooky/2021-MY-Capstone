import cv2

import json
import base64
import requests

count = 1

image = cv2.imread("namecard.jpg")

x_ocr_secret = "ZlBWaUFqdFp4bVFZTUpnTHZucGVwZFVOZUt3cllVY0o="
ocr_invoke_url = "https://f04b1d88f83e41a6b1df8ce399b61fb5.apigw.ntruss.com/custom/v1/9782/eed9df9be97433637c2950146e96ff0956759904a38b1e5e6a9a69a7f6691a68/general"

headers = {
    "Content-Type" : "application/json"
    "X-OCR-SECRET" : X-OCR-SECRET
    }

data = {
        "images" : [
            {
                "format" : "png"
                "name" : "sample_image_{}".format(count),
                "data" : null,
                "url" : 
                }
            ]
        }