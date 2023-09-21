import datetime
from flask import render_template, request ,redirect, make_response
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
from models import *
import json 
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dao import *
from time import perf_counter_ns

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='/login'

# ----------------------MAIL--------------------------------------#
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS = 'team@bloglite.com'
SENDER_PASSWORD = ''

def send_mail(receiver="yashsrivastava0211@gmail.com", message="Hi this is body of mail", subject= "From BlogSite"):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SENDER_ADDRESS
    msg['To'] = receiver
    msg.attach(MIMEText(message, 'html'))

    s = smtplib.SMTP(host= SERVER_SMTP_HOST, port= SERVER_SMTP_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    print("EMAIL SENT")
# ---------------------------MAIL END-------------------------------------#

@login_manager.user_loader
def load_user(id):
    u= user.query.get(int(id))
    return u

@app.route('/', methods=["GET", "POST"])
def dashboard():
    return redirect("/home")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=="GET":
        if current_user.is_active:
            return redirect("/home")
        return render_template('login.html')
    else:
        data = json.loads(request.data)
        username = data.get("username", None)
        password = data.get("password", None)
        u_obj= get_user(username)
        if u_obj is not None and check_password_hash(u_obj.password, password):
            if not current_user.is_active:
                login_user(u_obj)
            return {"access_token":"FakeToken"}
        return {}

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    res = app.make_response(redirect("/home"))
    res.set_cookie("username", " ", expires=0)
    logout_user()
    return redirect("/home")

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method=="GET":
        return render_template("create_user.html")
    else:
        data = json.loads(request.data)
        username = data.get("username", None)
        email = data.get("email", None)
        password = data.get("password", None)
        print("DATA RECEIVED: ", username, email, password)
        message= alreadyExist(username,email)
        if message:
            return {"message":message}

        u_obj= create_user_dao(username, email, password)
        login_user(u_obj)
        welcomeMsg= "Hello! Welcome to the BlogSite app. We hope you will enjoy using the app"
        send_mail(receiver=email ,message=welcomeMsg, subject= "Welcome !!" )
        
        return {"access_token": "FakeToken", "message":""}

@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    if request.method == "GET":
        if not current_user.is_active:
            return redirect("/login")
        return render_template("home.html")
    data = json.loads(request.data)
    username = data.get("username", None)
    start= perf_counter_ns()
    posts= get_home_posts(username)
    stop= perf_counter_ns()
    dict= {"posts":[]}
    for post in posts[-1::-1]:
        obj= {}
        obj["author"]= post.author
        print(post.author)
        obj["title"]= post.title
        obj["caption"]= post.caption
        obj["datetime"]= post.datetime
        obj["id"]= post.id
        obj["showComm"]= False
        obj["comments"]=[]
        obj["showCommentForm"]=False
        id= user.query.filter_by(username=post.author).first().id
        obj["userid"]= id
        obj["ispic"]= os.path.exists(f"static/img/propics/{id}.jpg")
        dict["posts"].append(obj)
    return dict

@app.route('/getComments', methods=["POST"])
def getComments():
    data = json.loads(request.data)
    postid = data.get("id", None)
    comms= get_Comments(postid)
    dict={"comments":[]}
    for comm in comms:
        obj={}
        obj["id"]= comm.id
        obj["author"]=comm.author
        obj["caption"]=comm.caption
        id= user.query.filter_by(username=comm.author).first().id
        obj["userid"]= id
        obj["ispic"]= os.path.exists(f"static/img/propics/{id}.jpg")

        dict["comments"].append(obj)
    return dict

@app.route('/addComment', methods=["POST"])
def addComment():
    data = json.loads(request.data)
    postid = data.get("postid", None)
    username= current_user.username
    caption= data.get("caption", None)
    comm_id= add_Comment(username, postid, caption)
    id= user.query.filter_by(username=username).first().id
    ispic= os.path.exists(f"static/img/propics/{id}.jpg")
    dict={"comment":{ "id":comm_id, "author":username, "caption": caption, "userid":"", "ispic": False,
                     "userid": id, "ispic": ispic}}
    return dict

@app.route('/deleteComment', methods=["POST"])
def deleteComment():
    data = json.loads(request.data)
    id = data.get("commentid", None)
    delete_Comment(id)
    return {}

@app.route('/search', methods=["GET", "POST"])
@login_required
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        data = json.loads(request.data)
        name = data.get("username", None)
        users= search_dao(name)
        names= []
        for user in users:
            names.append(user.username)
        return {"names": names}

@app.route('/users/<name>', methods=["GET", "POST"])
@login_required
def userinfo(name):
    if request.method == "GET":
        if get_user(name) is None:
            return redirect("/home")
        return  render_template("users.html")
    else:
        data = json.loads(request.data)
        name = data.get("username", None)
        e= get_user(name)
        if e is None:
            return {"err": "User not Found"}
        start= perf_counter_ns()
        followers= get_followers(name)
        followings= get_followings(name)
        posts= get_posts(name)
        stop= perf_counter_ns()
        dict= {"posts":[]}
        for post in posts[-1::-1]:
            obj= {}
            obj["author"]= post.author
            obj["title"]= post.title
            obj["caption"]= post.caption
            obj["datetime"]= post.datetime
            obj["id"]= post.id
            obj["showComm"]= False
            obj["comments"]=[]
            obj["showCommentForm"]=False
            dict["posts"].append(obj)
        dict["followers"]= followers
        dict["followings"]= followings
        dict["userid"]= e.id
        dict["err"]= ""
        ispic= os.path.exists(f"static/img/propics/{e.id}.jpg")
        dict["ispic"]=  ispic
        return dict

@app.route('/follow', methods=["POST"])
def follow():
    data = json.loads(request.data)
    person = data.get("person", None)
    other = data.get("other", None)
    flag = data.get("flag", None)
    if flag:
        # Unfollow
        unfollow_dao(person, other)
    else:
        # follow
        follow_dao(person, other)
    return {}

@app.route('/upload', methods=["GET", "POST"])
@login_required
def upload():
    if request.method=="GET":
        return render_template("upload.html")
    else:
        last_post = post.query.order_by(post.id.desc()).first()
        username= current_user.username
        filename= ""
        try:
            filename = str(last_post.id + 1)
        except:
            filename= "1"
        file = request.files["file"]
        title = request.form["title"]
        content = request.form["content"]
        p= "./static/img/posts/"+ filename+".jpg"
        file.save(os.path.join(p))
        upload_post(username,filename,content,title)
        return redirect("/myaccount")

@app.route('/myaccount', methods=["GET", "POST"])
@login_required
def myaccount():
    return render_template("myaccount.html")

@app.route('/editpost/<postid>', methods=["GET", "POST"])
@login_required
def editpost(postid):
    if request.method=="GET":
        if get_post(postid) is None:
            return redirect("/myaccount")
        return render_template("editpost.html")
    else:
        file = request.files["file"]
        title = request.form["title"]
        caption = request.form["caption"]
        postid = request.form["postid"]

        p= "./static/img/posts/"+ postid+".jpg"
        file.save(os.path.join(p))

        edit_post(postid,title,caption)
        return redirect("/myaccount")
        
@app.route('/deletepost/<postid>', methods=["POST", "GET"])
@login_required
def deletepost(postid):
    result = delete_post(postid,current_user.username)
    if result: 
        return redirect("/myaccount")
    else:
        # Change this and display the message "This post cannot be deleted by you" 
        return redirect("/myaccount")


@app.route('/getpost', methods=["POST"])
@login_required
def getpost():
    if request.method=="POST":
        data = json.loads(request.data)
        postid = data.get("postid", None)
        author, title, caption= get_post(postid)
        return {"author":author,"title": title, "caption":caption}


@app.route('/editprofile', methods=["GET", "POST"])
@login_required
def editProfile():
    if request.method=="GET":
        return render_template("editprofile.html")
    else:
        data = json.loads(request.data)
        msg = data.get("message", None)
        username = data.get("username", None)
        password = data.get("password", None)
        u_obj=get_user(username)
        if not check_password_hash(u_obj.password, password):
            return {"err":True}
        
        if msg=="EditUsername":
            newname = data.get("newname", None)
            if get_user(newname):
                return {"username_already_exist":True}
            u_obj.username= newname
            db.session.commit()
            change_data(username, newname)
            res = app.make_response(redirect("/home"))
            res.set_cookie("username",newname, expires="Mon, 01 Jan 2024 00:00:00 GMT")
            welcomeMsg= "Hello! Your username has been changed! Kindly contact us if it wasn't you"
            send_mail(receiver=u_obj.email ,message=welcomeMsg, subject= "Username Changed!")

        elif msg=="EditEmail":
            newemail = data.get("email", None)
            if get_user_by_email(newemail):
                return {"email_already_exist":True}
            u_obj.email= newemail
            db.session.commit()
            welcomeMsg= "Hello! Your email has been changed! Kindly contact us if it wasn't you"
            send_mail(receiver=u_obj.email ,message=welcomeMsg, subject= "Email Changed !")

        elif msg=="EditPassword":
            newpassword = data.get("newpassword", None)
            u_obj.password= generate_password_hash(newpassword, method='sha256')
            welcomeMsg= "Hello! Your password has been changed! Kindly contact us if it wasn't you"
            send_mail(receiver=u_obj.email ,message=welcomeMsg, subject= "Password Changed !")
            db.session.commit()
            logout()

        elif msg=="GetData":
            from models import post
            filepathname= "./static/csvdatafiles/"+ username+".csv"
            f = open(filepathname, 'w')
            header = "Serial No.,id,datetime,title,caption,no. of comments"
            f.write(header + "\n")
            posts = post.query.filter_by(author=username).all()
            sn=1
            for post in posts:
                numComments= len(list(comment.query.filter_by(post=post.id).all()))
                f.write(f"{sn},{post.id},{post.datetime},{post.title},{post.caption},{numComments}\n")
                sn += 1
            f.close()
            return {"err": False, "download":True}
        else:
            delete_data(username)
            db.session.delete(u_obj)
            db.session.commit()
            logout()
        return {"err": False}

@app.route('/upload_profile_pic', methods=["POST"])
@login_required
def upload_profile_pic():
    print("upload_profile_pic Function Reached !")
    file = request.files['profile_pic']
    id= str(current_user.id)
    p= "./static/img/propics/"+ id +".jpg"
    file.save(os.path.join(p))
    return redirect("/myaccount")

@app.route('/delete_pro_pic', methods=["POST"])
@login_required
def delete_pro_pic():
    print("delete_pro_pic Function Reached !")
    id= str(current_user.id)
    p= "./static/img/propics/"+ id +".jpg"
    os.remove(p)
    return redirect("/myaccount")
 
app.run(port=3000)