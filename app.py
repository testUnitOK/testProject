from flask import Flask,request,session,redirect
from flask import render_template,request
import psycopg2

app = Flask(__name__)
app.secret_key='m9XE4JH5dBOQ'
@app.route('/')
def index():
   return redirect('/login')

@app.route('/login')
def login():
    return render_template('index.html')
    

@app.route('/check_login',methods=['POST'])
def check_login():
    user,pw=(None,None)
    if 'user' in request.form:
        user=request.form['user']
    if 'pw' in request.form:
        pw=request.form['pw']
    if (user is None) or (pw is None):
        return redirect('/')
    if try_login(user,pw)==False:
        return show_error_msg('ユーザもしくはパスワードが違います')
    return redirect('/private')

@app.route('/private')
def private_page():
    return render_template('news.html',msg=session['login'])

@app.route('/logout')
def logout_page():
    try_logout()
    return show_msg('ログアウトしました')

def is_login():
    if 'login' in session:
        return True
    return False

def try_login(user,password):
    try :
     conn = psycopg2.connect(
                dbname="pythonTest", 
                user="postgres",
                password="postgre",
                host="db",
                port="5432"
            )
     print("接続成功")
     cur = conn.cursor()
     sql="select name from users where name=%s and password=%s"
     param=(user,password)
     cur.execute(sql,param)
     content= cur.fetchall()
     if len(content) == 0:
        return False
     session['login']=content[0][0]
     return True
    except Exception as e:
     print("接続失敗",e)
     raise

def try_logout():
    session.pop('login',None)
    return True

def show_msg(msg):
    return render_template('index.html',showMsg=msg)

def show_error_msg(msg):
    return render_template('index.html',errorMsg=msg)

if __name__=='__main__':
    app.run(host='0.0.0.0')
