from app import app
from flask import jsonify,request
# @app.route("/user")
# def user():
#     return"User Profile!"
from model.user_model import user_model
from datetime import datetime

from flask import request, send_file

obj = user_model()
# @app.route("/user/signup")
# def user_signup_controller():
#     return obj.user_Signup_model()
@app.route("/user/getall", methods = ["GET"])
def user_getall_controller():
    return obj.user_getall_model()

@app.route("/user/addone", methods = ["POST"])
def user_addone_controller():
    data = request.json
    return obj.user_addone_model(data)

@app.route("/user/update", methods = ["PUT"])
def user_update_controller():
    data = request.json
    return obj.user_update_model(data)

@ app.route("/user/delete/<id>", methods = ["DELETE"])
def user_delete_controller(id):
    return obj.user_delete_model(id)

@app.route("/user/getall/limit/<limit>/page/<page>", methods = ["GET"])
def user_pagination_controller(limit,page):
    return obj.user_pagination_model(limit,page)

@app.route("/user/<id>/upload/avatar", methods=["PUT"])
def user_upload_avatar_controller(id):
    if 'avatar' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    unique_filename = str(datetime.now().timestamp()).replace(".", "")
    filename_split = file.filename.rsplit('.', 1)
    ext = filename_split[-1]
    final_file_path = f"Uploads/{unique_filename}.{ext}"
    file.save(final_file_path)
    return obj.user_upload_avatar_model(id, final_file_path)
    
@app.route("/uploads/<filename>")
def user_getavatar_controller(filename):
    return send_file(f"uploads/{filename}")    

@app.route("/user/login", methods = ["POST"])
def user_login_controller():
    data = request.json
    return obj.user_login_model(data)

