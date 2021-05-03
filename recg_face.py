#读取utility.origin_face_path/utility.image_cnt.png
#识别图中的人脸并标识，存入recg_face.res_face_path/recg_face.image_cnt.png
#识别的结果存入recg_face.reslist
import numpy as np
from PIL import Image,ImageDraw
import face_recognition, os, utility


known_face_path = "known_faces"
known_face_encodings = []
known_face_names = [
    "Guoguo", "Guoguo", "Guoguo", "Guoguo","Guoguo", "Guoguo", "Guoguo",
    "Shengsheng", "Shengsheng",
    "Haoge", "Haoge", "Haoge",
    "Zege", "Zege", "Zege",
    "Sange", "Sange"
]
recg_res = False
res_face_path = "res_imgs"
image_cnt = 0 #res_face
reslist = []

def get_known_faces():
    global known_face_path
    global known_face_encodings
    known_face_encodings.clear()
    for root,dirs,files in os.walk(known_face_path):
        for f in sorted(files):
            fullname = os.path.join(root,f) 
            known_image = face_recognition.load_image_file(fullname)
            #print(fullname)
            known_face_encoding = face_recognition.face_encodings(known_image)[0]
            known_face_encodings.append(known_face_encoding)

def update_image_cnt():
    global image_cnt
    files = os.listdir(res_face_path)
    image_cnt = len(files)

def recognize_face():
    #获取基准人脸
    get_known_faces()
    global known_face_encodings
    global known_face_names
    global recg_res
    #读取要处理的人脸
    unknown_image = face_recognition.load_image_file(f"{utility.origin_face_path}/{utility.image_cnt}.jpg")
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image,face_locations)
    pil_image = Image.fromarray(unknown_image)
    draw = ImageDraw.Draw(pil_image)
    #init
    reslist.clear()
    recg_res = False
    #遍历基准人脸进行比对
    for(top,right,bottom,left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4) #一个bool list
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances) #取距离最小的
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        reslist.append(name)
        recg_res = True
        #在图上标出人脸
        draw.rectangle(( (left,top),(right,bottom) ), outline = (255,0,0))
        #标注姓名
        text_width, text_height = draw.textsize(name)
        draw.rectangle( ((left, bottom-text_height-2),(right,bottom)), fill = (255,0,0), outline = (255,0,0) )
        draw.text( (left+6, bottom-text_height-1), name, fill = (255,255,255) )
    update_image_cnt()
    pil_image.save(f"{res_face_path}/{image_cnt}.jpg")


