#encoding:utf-8

import base64
import time
from flask import Flask
from flask import jsonify
from flask import request
import face_recognition
import json
import numpy as np
import pymysql
import warnings


warnings.filterwarnings(action='ignore')


conn = pymysql.connect(host='localhost',user='root', password='haifan123', database='face', charset='utf8')
cursor = conn.cursor()
app = Flask(__name__)




@app.route("/face/search",methods=['POST'])
def faceSearch():

    data = request.get_json()
    userFace = data['userFace']
    baseToimg(userFace)
    #start1 = time.clock()
    
    image = face_recognition.load_image_file("src.jpg")
    srcData = face_recognition.face_encodings(image)[0]
    #elapsed1 = (time.clock() - start1)
    #print("Time used1aa:",elapsed1)
    srcDataList = [srcData]
    index = -1
    pName = ""
    counts = int(faceCounts())
    if counts == 0:
        index = -1
    else:
         for i in range(1, counts+1):

            feature = faceSelectById(i)
     #       start = time.clock() 
            results = face_recognition.compare_faces(srcDataList, np.array(feature), 0.3)
      #      elapsed = (time.clock() - start)
       #     print("Time used:",elapsed)
            if results[0] == True:
                pName = faceDataById(i)
                index = 1
                break
            elif i == counts+1:
                index = -1
    if index == -1:
        return jsonify({'code': '-1', 'msg': '人脸库未存在该人脸'})
    else:
        return jsonify({'code': '0', 'msg': '已查询到该人脸','name' : pName})




@app.route("/face/add",methods=['POST'])
def faceAdd():
    data = request.get_json()
    userName = data['userName']
    userCard = data['userCard']
    userFace = data['userFace']
    baseToimg(userFace)
    image = face_recognition.load_image_file("src.jpg")
    featureData = face_recognition.face_encodings(image)[0]
    query = """insert into user1(userName,userCard,userFace) values (%s,%s,%s)"""
    values = (str(userName),str(userCard),featureData.tostring())
    conn.commit()
    if int(cursor.execute(query, values)) == 1:
        return jsonify({'code': '0', 'msg': '添加用户成功'})
    else: return jsonify({'code': '-1', 'msg': '添加用户失败'})



@app.route("/face/delete",methods=['POST'])
def faceDelete():
    data = request.get_json()
    id = data['userId']
    if int(cursor.execute('delete from user1 where id = %s', ([id]))) == 1:
        return jsonify({'code': '0', 'msg': '删除人脸成功'})
    else:return jsonify({'code': '-1', 'msg': '删除人脸失败'})
    conn.commit()



def faceCounts():
    query = ('select count(id) from user1')
    cursor.execute(query)
    (counts,) = cursor.fetchone()
    counts = str(counts)
    conn.commit()
    return counts



def faceSelectById(id):
    cursor.execute('select userFace from user1 where id = %s', ([id]))
    values = cursor.fetchall()
    feature = np.frombuffer(values[0][0])
    return feature


def faceDataById(id):
    cursor.execute('select userName from user1 where id = %s', ([id]))
    values = cursor.fetchall()
    username = values[0][0]
    username = str(username)
    return username



def baseToimg(base):
    base1 = base.replace('data:image/jpeg;base64,','')
    imgdata = base64.b64decode(base1)
    file = open('src.jpg','wb')
    file.write(imgdata)
    file.close()
    return base1


if __name__ == '__main__':
    app.run(port=8888,host='0.0.0.0',debug=False,threaded=True)
