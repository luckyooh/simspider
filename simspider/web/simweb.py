import json
import mimetypes

from flask import Flask, render_template, request, url_for, send_from_directory, send_file, make_response
import redis
import os

from werkzeug.utils import secure_filename

cache_dir = "/Users/jiangfubang/Documents/project/ai/simspider/simspider/临时目录/"
all_dir = "/Users/jiangfubang/Documents/project/ai/simspider/simspider/待处理/"
dealed_dir = "/Users/jiangfubang/Documents/project/ai/simspider/simspider/已处理/"
conf_file = "/Users/jiangfubang/Documents/project/ai/simspider/simspider/conf.py"

app = Flask(__name__)

host = "127.0.0.1"

@app.route("/")
def index():
    msg = {}
    # 未处理
    unmsg = undeal()
    # 处理中
    msging = dealing()
    # 已处理
    msged = dealed()

    msg.update(unmsg)
    msg.update(msging)
    msg.update(msged)

    return render_template("index.html", **msg)

def undeal():
    all_files = os.listdir(all_dir)
    cache_files = os.listdir(cache_dir)
    un_files = list(set(all_files)-set(cache_files))
    msg = {
        "undeals": un_files,
    }
    return msg

def dealed():
    dealed_files = os.listdir(dealed_dir)
    msg = {
        "dealeds": dealed_files,
    }
    return msg

def dealing():
    cache_files = os.listdir(cache_dir)
    dealed_files = os.listdir(dealed_dir)
    dealing_files = list(set(cache_files)-set(dealed_files))
    msg = {
        "dealings": dealing_files,
    }
    return msg

@app.route("/show_upload")
def show_load_file():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if f:
        filename = f.filename
        print(filename)
        types = ["txt"]
        if filename.split(".")[-1] in types:
            f.save("/Users/jiangfubang/Documents/project/ai/simspider/simspider/待处理/{}".format(filename))
            return json.dumps({"msg": "上传成功", "code": 200})
        else:
            return json.dumps({"msg": "文件格式不合法", "code": 400})
    else:
        return json.dumps({"code":405, "msg": "请求方式不正确"})

@app.route("/download/<path:filename>")
def download(filename):
    print(filename)
    dir = "/Users/jiangfubang/Documents/project/ai/simspider/simspider/已处理/"
    response = make_response(send_file(dir+filename, as_attachment=True))
    mime_type = mimetypes.guess_type(filename)[0]
    response.headers["Content-Type"] = mime_type
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)