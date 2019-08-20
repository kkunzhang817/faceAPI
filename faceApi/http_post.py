import requests
import json
import os
import base64


headers = {
    "Content-Type": "application/json;",
    }



def postAdd():
    url = "http://10.0.0.61:8888/face/add"
    path ='/media/haifan/bf6bce98-98ec-49b2-b525-f5a19045ff9a/faceAPI/imgSave/face/imgs/'
    imgs = os.listdir(path)
    for i in range(0,len(imgs)):
        base = imgTobase(path+imgs[i])
        if len(imgs[i]) == 18:
           userName = "zkk"
           userCard = "111111111111111111"
        else:
           userCard = imgs[i].split(".")[0].split("_")[1]
           userName = imgs[i].split(".")[0].split("_")[2]


        pyload = {"userName":userName,"userCard":userCard,"userFace":base}
        response = requests.post(url, data=json.dumps(pyload), headers=headers).text
        print(response)

def postDel():
    url = "http://10.0.0.61:8888/face/delete"
    pyload = {"userId": "121"}
    response = requests.post(url, data=json.dumps(pyload), headers=headers).text
    print(response)



def imgTobase(imgPath):
    with open(imgPath, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        return s


if __name__ == '__main__':
    postAdd()






