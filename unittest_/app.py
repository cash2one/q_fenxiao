#encoding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import flask_admin as admin
from flask_admin.contrib import sqla


# Create application
app = Flask(__name__)


# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:111111@127.0.0.1:3306/haitao?charset=utf8"
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


# class Users(db.Model):
#
#     """
#     用户信息
#     """
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     # gmt_created = db.Column(db.DateTime,doc='创建时间')
#     # gmt_modified = db.Column(db.DateTime,doc='最后更新时间')
#     # deleted = db.Column(db.Boolean,default=0,doc='记录状态 0 删除 1 正常')
#
#     uid = db.Column(db.String(128))
#     nick = db.Column(db.String(128))
#     email = db.Column(db.String(128))
from models.user_do import Users
class UsersAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns= ['id','uid','nick','email']
    column_labels = {
    'id': '用户名',
    'uid': '姓名',
    'nick': '注册时间'
    }

# Create admin
admin = admin.Admin(app, name='Flask后台管理测试:SQLAlchemy2', template_mode='bootstrap3')
admin.add_view(UsersAdmin(Users, db.session))

if __name__ == '__main__':

    # Create D
    # Start app
    #db.create_all()
    #db.create_all()
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app.run(port=5001)