import requests
import json
import cv2

# addr = 'http://localhost:8080/'
addr = 'https://testservice-476rxuzmhq-ew.a.run.app'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

img = cv2.imread('known_faces/obama.jpg')

# Resize frame of video to 1/4 size for faster face recognition processing
small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
img = small_frame[:, :, ::-1]


# encode image as jpeg
_, img_encoded = cv2.imencode('.jpg', img)
# send http request with image and receive response
response = requests.post(addr, data=img_encoded.tostring(), headers=headers)
# decode response
# print(json.loads(response.text))
print(response.text)

# expected output: {u'message': u'image received. size=124x124'}