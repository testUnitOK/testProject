from flask import Flask,request,session,redirect
import psycopg2


app = Flask(__name__)
app.secret_key='m9XE4JH5dBOQ'
@app.route('/')
def index():
   return """
   <html><body><h2>ログインフォーム</h2>
   <form action="check_login" method="POST">
   ユーザ名：<br>
   <input type="text" name="user"><br>
   パスワード:<br>
   <input type="password" name="pw">
   <input type="submit" value="ログイン">
   </form>
   """

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
        return """
       <h1>ユーザ名もしくはパスワードが間違いです</h1>
       <p><a href="/">戻る</a><p> 
       """
    return redirect('/private')

@app.route('/private')
def private_page():
    if not is_login():
        return """
        <h1>ログインしてください</h1>
        <p><a href="/">ログイン画面に戻る</a></p>
        """
    return """
    <h1>ようこそ"""+session['login']+"""さん</h1>
    <p>あなたはログイン中です</p>
    <p><a href="/logout">ログインアウト</a></p>
    """

@app.route('/logout')
def logout_page():
    try_logout()
    return """
    <h1>ログアウトしました</h1>
    <p><a href="/">戻る</a/></p>
    """

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
     if content ==None:
        return False
     session['login']=content[0][0]
     return True
    except Exception as e:
     print("接続失敗",e)
     raise
def try_logout():
    session.pop('login',None)
    return True

if __name__=='__main__':
    app.run(host='0.0.0.0')





