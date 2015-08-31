from flask import Flask, render_template, request
import os
import json
from nova_code import start_vm
from swift_code import upload_to_container, check_file_exists

container_upload = 'uploads'
container_download = 'rendered'
environ = json.load(open(os.environ['CRED_FILE']))['CONFIG']['CONFIG_VARS']

app = Flask(__name__)
app.debug = True


@app.route("/example", methods=['GET', 'POST'])
def example(btn_clicked=""):
    if request.method == 'POST':
        filename = request.form['files']
        mail = request.form['mail']
        f = open("examples/" + filename, 'r')
        obj_name = upload_to_container(f, container_upload, environ)
        start_vm(container_upload, obj_name, container_download, environ, mail)
        return render_template('upload.jinja', btn_clicked=obj_name)
    else:
        files = os.listdir("examples")
        return render_template('upload.jinja', btn_clicked='example', files=files)


@app.route("/")
@app.route('/upload', methods=['GET', 'POST'])
def upload_file(btn_clicked=""):
    if request.method == 'POST':
        f = request.files['FileToUpload']
        mail = request.form['mail']
        obj_name = upload_to_container(f, container_upload, environ)
        start_vm(container_upload, obj_name, container_download, environ, mail)
        return render_template('upload.jinja', btn_clicked=obj_name)
    else:
        return render_template('upload.jinja', btn_clicked='no')


@app.route('/file/<filename>')
def show_output(filename):
    if check_file_exists(filename, container_download, environ):
        return render_template('download.jinja', filename=filename)
    else:
        return render_template('wait.jinja', filename=filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ['PORT']))
