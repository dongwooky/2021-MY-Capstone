import cv2
import sys

def on_trackbar(pos, frame_unnoise):
    bsize = pos
    if bsize % 2 == 0:
        bsize = bsize - 1
    if bsize < 3:
        bsize = 3
        
    dst = cv2.adaptiveThreshold(frame_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                cv2.THRESH_BINARY, bsize, 5)
    
    cv2.imshow('dst', dst)

capture = cv2.VideoCapture(1)

if not capture.isOpened():
    print('Camera open failed!')
    sys.exit()
    
while True:
    ret, frame = capture.read()
    
    if not ret:
        print('Frame read error!')
        sys.exit()
        
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_unnoise = cv2.bilateralFilter(frame_gray, -1, 10, 5)
    _, frame_binary = cv2.threshold(frame_unnoise, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(frame_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    for points in contours:
        if cv2.contourArea(points) < 1000:
            continue
    
        approx = cv2.approxPolyDP(points, cv2.arcLength(points, True) * 0.02, True)
        
        if len(approx) != 4:
            continue
        
        cv2.polylines(frame, points, True, (0, 0, 255), thickness = 3)
        
    cv2.imshow('frame', frame)
    cv2.imshow('frame_unnoise', frame_unnoise)
    cv2.imshow('frame_binary', frame_binary)
    
    cv2.namedWindow('dst')
    cv2.createTrackbar('Block size', 'dst', 0, 200, on_trackbar(frame_unnoise))
    cv2.setTrackbarPos('Block size', 'dst', 11)
    
    if cv2.waitKey(33) == ord('q'):
        break
    
capture.release()
cv2.destroyAllWindows()