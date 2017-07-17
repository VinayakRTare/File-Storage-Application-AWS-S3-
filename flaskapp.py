
import os
from flask import Flask, request, make_response,render_template
import boto3
import datetime
from botocore.client import Config
import codecs

app = Flask(__name__)

ACCESS_KEY_ID = '***********************'
ACCESS_SECRET_KEY = '***********************'
BUCKET_NAME = 'vin21-**************'
FILE_NAME = 'test.jpg';

s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY_ID,
                    aws_secret_access_key=ACCESS_SECRET_KEY,config= boto3.session.Config(signature_version='s3v4'))
client = boto3.client('s3')
resource = boto3.resource('s3')

app.secret_key='any string'
mypath = '*******************************'

@app.route('/')
def hello_world():
    return render_template('login.html')

@app.route('/login',methods = ['POST','GET'])
def login():git push -u origin master
    key = 'login1.txt'
    bucket = s3.Bucket('vin21-bucket')
    for obj in bucket.objects.all():
        if key == obj.key:
            body = obj.get()['Body'].read().decode('utf-8')
            print(body)
            i = 0
            list = []
            list = body.split(';')
            for line in list:
                    print(line)
                    username, password = line.split(':')
                    username = username.strip()
                    print(username)
                    passwd = password.strip()
                    print(passwd)
                    # print(request.form['ID'])
                    # print(request.form['Password'])
                    if request.form['username'] == username and request.form['password'] == passwd:
                        i = 1
                        print("hello")
                        break
    if i == 0:
        return render_template('login.html')
    else:
        return render_template('index.html')

@app.route('/uploadpage', methods=['POST'])
def menu2():
    return render_template('upload.html')

@app.route('/downloadPage', methods=['POST'])
def menu3():
    return render_template('download.html')
@app.route('/index', methods=['POST'])
def index():
    return render_template('index.html')
@app.route('/deletePage', methods=['POST'])
def menu4():
    return render_template('delete.html')

@app.route('/showImagePage', methods=['POST'])
def menu5():
    return render_template('showImagePage.html')
@app.route('/showTextFile', methods=['POST'])
def menu6():
    return render_template('showTextPage.html')

@app.route('/showText', methods=['POST'])
def showText():
    KEY = request.form['filename']
    bucket = s3.Bucket('vin21-bucket')
    for obj in bucket.objects.all():
        if KEY == obj.key:
            body = obj.get()['Body'].read()
            print(body)
            response = body
            return render_template('response.html',response=response)


@app.route('/localList', methods=['POST'])
def menu():
    list_of_files = []
    print("List of Files")
    for filename in os.listdir(mypath):
        fileinfo = {}
        fileinfo['filename'] = filename
        print(filename)
        list_of_files.append(fileinfo)
    return render_template('localList.html', fileList=list_of_files)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_name = file.filename
    content = file.read()
    s3.Bucket('vin21-bucket').put_object(Key=file_name, Body=content)
    return render_template('response.html', response = "Successfully uploaded")

@app.route('/download', methods=['POST'])
def download():
    BUCKET_NAME = 'vin21-*****************'  # replace with your bucket name
    KEY = request.form['filename']
    s3 = boto3.resource('s3')
    s3.Bucket(BUCKET_NAME).download_file(KEY, 'test4.jpg')
    return render_template('response.html', response ="Successfully Downloaded")

@app.route('/showImg', methods=['POST'])
def showImage():
    KEY = request.form['filename']
    response='https://s3.amazonaws.com/vin21-bucket/%s'%KEY
    return render_template('showImg.html', response =response)

@app.route('/list', methods=['POST'])
def list():
        obj = ''
        lw = 'Last write'
        for bucket in s3.buckets.all():
            for object in bucket.objects.all():
                obj = obj + '</br>' + object.key
                obj = obj + '&nbsp&nbsp' + str(object.size)
                obj = obj + '&nbsp&nbsp' + str(object.last_modified)
        return obj

@app.route('/delete', methods=['POST'])
def delete():
    file_name = request.form['filename']
    for bucket in s3.buckets.all():
        for object in bucket.objects.all():
            if object.key==file_name:
                object.delete()
                return "File has been deleted successfully"


if __name__ == '__main__':
    app.run(debug=True)

