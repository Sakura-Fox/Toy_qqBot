import numpy as np
from PIL import Image,ImageDraw
import face_recognition
import os


known_face_path = "known_faces"
known_face_encodings = []
for root,dirs,files in os.walk(known_face_path):
        for f in sorted(files):
            fullname = os.path.join(root,f)
            known_image = face_recognition.load_image_file(fullname)
            print(fullname)
            known_face_encoding = face_recognition.face_encodings(known_image)[0]
            known_face_encodings.append(known_face_encoding)