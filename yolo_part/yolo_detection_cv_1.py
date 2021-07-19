import sys
import numpy as np
import cv2

model = 'yolo_v3_416/yolov3.weights'
config = 'yolo_v3_416/yolov3.cfg'
class_labels = 'yolo_v3_416/coco.names'
confThreshold = 0.5
nmsThreshold = 0.4

#네트워크 생성
net = cv2.dnn.readNet(model, config)

if net.empty():
    print('Net Open failed!')
    sys.exit()
    
#클래스 이름 불러오기
classes = []
with open(class_labels, 'rt') as file:
    classes = file.read().rstrip('\n').split('\n')
    
colors = np.random.uniform(0, 255, size=(len(classes), 3))

#출력 레이어 이름 받아오기
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

#실행
image = cv2.imread('dog.jpg')

blob = cv2.dnn.blobFromImage(image, 1/255., (320, 320), swapRB=True)
net.setInput(blob)
outs = net.forward(output_layers)

h, w = image.shape[:2]

class_ids = []
confidences = []
boxes = []


for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > confThreshold:
            cx = int(detection[0] * w)
            cy = int(detection[1] * h)
            bw = int(detection[2] * w)
            bh = int(detection[3] * h)
            
            sx = int(cx - bw / 2)
            sy = int(cy - bh / 2)
            
            boxes.append([sx, sy, bw, bh])
            confidences.append(float(confidence))
            class_ids.append(int(class_id))
            
indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)

for i in indices:
    i = i[0]
    sx, sy, bw, bh = boxes[i]
    label = f'{classes[class_ids[i]]}: {confidences[i]:.2}'
    color = colors[class_ids[i]]
    cv2.rectangle(image, (sx, sy, bw, bh), color, 2)
    cv2.putText(image, label, (sx, sy - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)
    
t, _ = net.getPerfProfile()
label = 'Inference time: %.2f ms' %(t * 1000.0 / cv2.getTickFrequency())
cv2.putText(image, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (0, 0, 255), 1, cv2.LINE_AA)

cv2.imshow('image', image)
cv2.waitKey()
    
cv2.destroyAllWindows()