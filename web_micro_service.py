import os
import numpy as np
import cv2
import face_recognition
import glob
import json
from flask import Flask, request, Response
from flask import abort


app = Flask(__name__)

known_face_file_list = glob.glob("known_faces/*.jpg")

known_face_encodings = []
known_face_names = []

for known_face_file_path in known_face_file_list:
    # Load a sample picture and learn how to recognize it.
    face_image = face_recognition.load_image_file(known_face_file_path)
    face_encoding = face_recognition.face_encodings(face_image)[0]

    image_filename = os.path.splitext(os.path.basename(known_face_file_path))[0]

    # Add known face encodings and their names
    known_face_encodings.append(face_encoding)
    known_face_names.append(image_filename)

# Initialize some variables
face_locations = []
face_encodings = []


@app.route('/', methods=['POST', 'GET'])
def find_person_in_frame():

    #### FIRST CHECK THE INPUTS ####
    content_type = request.headers['content-type']
    if content_type != 'image/jpeg':
        abort(406)

    nparr = np.fromstring(request.data, np.uint8)
    # decode image
    output = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)

    # Loop over each face found in the frame to see if it's someone we know.
    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Stranger"

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        face_names.append(name)

    # if len(face_names) == 1:
    #     name = face_names[0]
    #     print("I see someone named {}!".format(name))
    # elif len(face_names) > 1:
    #     print("Found {} people, named {}!".format(len(face_names), face_names))

    response = {'people': face_names, 'message': 'image received. size={}x{}'.format(output.shape[1], output.shape[0])}

    return Response(response=json.dumps(response), status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
