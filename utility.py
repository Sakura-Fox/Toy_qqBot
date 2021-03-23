#mirai qq机器人 保存图片
import urllib.request
import os
origin_face_path = "mirai_imgs" #位于/home/lwx/Codes/Toy_qqBot下
image_cnt = 0 #当前要处理的图片

def update_image_cnt():
    global image_cnt
    files = os.listdir(origin_face_path)
    image_cnt = len(files)

def download_imgae(img_url):
    request = urllib.request.Request(img_url)
    global origin_face_path
    global image_cnt
    try:
        response = urllib.request.urlopen(request)
        update_image_cnt()
        img_name = f"{image_cnt}.jpg"
        filename = f"{origin_face_path}/{img_name}"
        if (response.getcode() == 200):
            with open(filename, "wb") as f:
                f.write(response.read()) # 将内容写入图片
            return filename
    except:
        return "download image failed"



