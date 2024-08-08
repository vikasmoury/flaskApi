import mysql.connector
import json
from flask import make_response
from flask import jsonify
from datetime import datetime, timedelta
import jwt
class user_model():
    # def user_Signup_model(self):
    #     return "This is User_SignUp_Model"
    def __init__(self):
        try:
            self.con = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "Vikas20@",
                database = "demo"
            )
            self.cur = self.con.cursor(dictionary = True)
            print("Connection Successfull")
        except:
            print("Some Error")

    def user_getall_model(self):
        try:
            self.cur.execute("SELECT * FROM users")
            result = self.cur.fetchall()
            if len(result)>0:
                return make_response({"payload":result},200)
            else:
                return make_response({"Message":"Data Not Found"}, 204)
        except mysql.connector.Error as err:
            return f"Error:{err}"
    
    def user_addone_model(self, data):
        try:
            sql = "INSERT INTO users(`id`, `name`, `phone`, `role`, `password`, `avatar`) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (data['id'], data['name'], data['phone'], data['role'], data['password'], data['avatar'])
            self.cur.execute(sql, values)
            self.con.commit()
            return make_response({"payload":"User Added Successfully"},201)
        except mysql.connector.Error as err:
            return make_response({"Message":f"Error:{err}"},204)
        
    def user_update_model(self, data):
        print("data in user_update_model<><><>")
        try:
            sql = "UPDATE users SET `name` = %s, `phone` = %s, `role` = %s, `password` = %s, `avatar` = %s WHERE id = %s"
            values = (data['name'], data['phone'], data['role'], data['password'], data['avatar'], data['id'])
            self.cur.execute(sql, values)
            self.con.commit()
            return make_response({"payload":"User Updated Successfully"},201)
        except mysql.connector.Error as err:
            return make_response({"Message":f"Error:{err}"},202)
        
    def user_delete_model(self, id):
        print("data in delete_model<><>")
        try:
            sql= "DELETE FROM users WHERE id = %s"
            self.cur.execute(sql, (id,))
            self.con.commit()
            if self.cur.rowcount>0:
                return make_response({"payload":"User Deleted Successfully"},200)
            else:
                return make_response({"Message":"User Not Found"}, 202)
        except mysql.connector.Error as err:
            return f"Error:{err}"
        
    def user_pagination_model(self,limit,page):
        limit = int(limit)
        page = int(page)
        start = (page*limit)-limit
        qry = f"SELECT * FROM users LIMIT {start}, {limit}"
        self.cur.execute(qry)
        result = self.cur.fetchall()
        if len (result)>0:
            return make_response(jsonify({"payload":result,"page_no":page, "limit":limit}),200)
        else:
            return make_response(jsonify({"Message":"No Data Found"}),404)
        
    def user_upload_avatar_model(self, id, filepath):
        try:
            self.cur.execute(f"UPDATE users SET avatar = '{filepath}' WHERE id = {id}")
            self.con.commit()
            if self.cur.rowcount>0:
                return jsonify({"Message":"File Uploaded Successfully"}), 201
            else:
                return jsonify({"Message":"Nothing to Update"}), 202
        except Exception as e:
            return jsonify({"error":str(e)}), 500
        finally:
            self.con.close()


    def user_login_model(self, data):
        self.cur.execute(f"SELECT id, name, email, phone, avatar, role_id FROM users WHERE email = '{data['email']}' AND password = '{data['password']}'")
        result = self.cur.fetchall()
        # return str(result[0])
        userdata = result[0]
        exp_time = datetime.now() + timedelta(minutes = 15)
        exp_epoch_time = int(exp_time.timestamp())
        # return str(exp_epoch_time)
        payload = {
            "payload": userdata,
            "exp": exp_epoch_time
        }
        jwtoken = jwt.encode(payload, "harry", algorithm= "HS256")
        return make_response({"token": jwtoken}, 200) 

    def close_connection(self):
        if self.cur:
            self.cur.close()
            if self.con:
                self.con.close()