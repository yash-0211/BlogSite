import datetime
from flask import render_template, request ,redirect, make_response, session
from models import *
import json 
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dao import *
import jwt
from functools import wraps

# ----------------------MAIL--------------------------------------------#
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS = 'team@bloglite.com'
SENDER_PASSWORD = ''
# function to send email to user
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

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token= request.headers.get('Authentication-Token') 
        if not token or token=="null":
            session['logged_in']= False
            return jsonify( {'Alert':'Token missing'} )
        try:
            payload= jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        except:
            session['logged_in']= False
            return jsonify( {'Alert':'Incorrect token'} )
        return func( payload,*args, **kwargs )  
    return decorated

@app.route('/', methods=["GET", "POST"])
def dashboard():
    return redirect("/home")

@app.route('/nav', methods=["POST"])
@token_required
def nav(token):
    return {"message":"Logged in", "username":token['username'] }

@app.route('/getname', methods=["POST"])
@token_required
def getname(token):
    return {"username": token['username']}

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if request.method=="GET":
    #     if session.get('logged_in'):
    #         print("Redirecting to home")
    #         return redirect("/home")
    #     return render_template('login.html')
    data = json.loads(request.data)
    username = data.get("username", None)
    password = data.get("password", None)
    print(username, password)
    u_obj= get_user(username)
    print(u_obj)
    # if u_obj is not None and check_password_hash(u_obj.password, password):
    if u_obj is not None and u_obj.password==password:
        session['logged_in']= True
        token= jwt.encode(
        payload= { 'username': username,
            'expiration': str(datetime.datetime.now()+ datetime.timedelta(seconds=120)) }
            , key= app.config['SECRET_KEY'])
        
        return {"access_token":token }
    return {}

@app.route('/logout', methods=["GET", "POST"])
@token_required
def logout(user):
    # delete token also
    session['logged_in']= False
    # return redirect("/home")
    return {}

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    # if request.method=="GET":
    #     if session.get('logged_in'):
    #         return redirect("/home")
    #     return render_template("create_user.html")
    data = json.loads(request.data)
    username = data.get("username", None)
    email = data.get("email", None)
    password = data.get("password", None)
    if " " in username:
        return {"message": " Whitespace is not allowed in username" }
    print("DATA RECEIVED: ", username, email, password)
    message= alreadyExist(username,email)
    if message:
        return {"message":message}
    session['logged_in']= True
    token= jwt.encode(
        payload= { 'username': username,
        'expiration': str(datetime.datetime.now()+ datetime.timedelta(seconds=120)) }
        , key= app.config['SECRET_KEY'])
    create_user_dao(username, email, password)
    print(token)
    
    welcomeMsg= "Hello! Welcome to the BlogSite app. We hope you will enjoy using the app"
    send_mail(receiver=email ,message=welcomeMsg, subject= "Welcome !!" )
    return {"access_token":token, "message":""}

@app.route('/home', methods=["GET"])
def home():
    return render_template("home.html")

@app.route('/home', methods=[ "POST"])
@token_required
def home_post(token):
    username = token['username']
    posts= get_home_posts(username)
    dict= { }
    posts= posts[-1::-1]
    posts= [post.id for post in posts]
    dict["more"]= len(posts)>5
    dict["posts"]= posts
    return dict

@app.route('/LoadMorePosts', methods=[ "POST"])
@token_required
def LoadMorePosts(token):
    username= token['username']
    data = json.loads(request.data)
    length = data.get("length")
    posts= get_home_posts(username)
    posts=  posts[-1::-1]
    if len(posts)< length+5:
        posts=  posts[length-1:length+5]
    else:
        posts= posts[length-1:]
    
    return {"posts": [post.id for post in posts]}

@app.route('/getComments', methods=["POST"])
def getComments():
    data = json.loads(request.data)
    postid = data.get("id", None)
    comms= get_Comments(postid)
    dict={"comments":[]}
    for comm in comms:
        id= user.query.filter_by(username=comm.author).first().id
        obj= {"id":comm.id, "author":comm.author, "caption":comm.caption, "userid":id,
              "ispic":os.path.exists(f"static/img/propics/{id}.jpg"),
            }
        dict["comments"].append(obj)
    return dict

@app.route('/addComment', methods=["POST"])
@token_required
def addComment(token):
    data = json.loads(request.data)
    postid = data.get("postid", None)
    username= token['username']
    newComment= data.get("newComment", None)
    print(newComment)
    comm_id= add_Comment(username, postid, newComment)
    id= user.query.filter_by(username=username).first().id
    ispic= os.path.exists(f"static/img/propics/{id}.jpg")
    dict={"comment":{ "id":comm_id, "author":username, "caption": newComment, "userid":"", "ispic": False,
                     "userid": id, "ispic": ispic}}
    return dict

@app.route('/deleteComment', methods=["POST"])
@token_required
def deleteComment(token):
    data = json.loads(request.data)
    id = data.get("commentid", None)
    delete_Comment(id)
    return {}

@app.route('/search', methods=["GET", "POST"])
def search():
    # if request.method == "GET":
    #     return render_template("search.html")
    # else:
    data = json.loads(request.data)
    name = data.get("username", None)
    users= search_dao(name)
    names= []
    for user in users:
        names.append(user.username)
    return {"names": names}


@app.route('/users/<name>', methods=["GET", "POST"])
def userinfo(name):
    # if request.method == "GET":
    #     try:
    #         username= request.cookies['username']
    #     except:
    #         username= None
    #     if get_user(name) is None: return redirect("/home")
    #     if name==username: return redirect("/myaccount")
    #     return render_template("users.html")
    print("In users page")
    
    e= get_user(name)
    if not e: return {}
    followers= get_followers(name)
    followings= get_followings(name)
    posts= get_posts(name)
    dict= {"posts":[p.id for p in posts], "followers":followers, "followings":followings, "userid":e.id, "err":""}
    dict["ispic"]=  os.path.exists(f"static/img/propics/{e.id}.jpg")
    return dict

@app.route('/follow', methods=["POST"])
@token_required
def follow(token):
    data = json.loads(request.data)
    person = token['username']
    other = data.get("other", None)
    f_obj= follower.query.filter_by(person=person,following=other).first()
    if f_obj:
        print("UNFOLLOWED !!")
        db.session.delete(f_obj)
        db.session.commit()
    else:
        print("FOLLOWED !!")
        follow_dao(person, other)
    return {}

# @app.route('/upload', methods=["GET"])
# def upload_get():
#     return render_template("upload.html")

@app.route('/upload', methods=["POST"])
@token_required
def upload(token):
    last_post = post.query.order_by(post.id.desc()).first()
    username= token['username']
    filename= ""
    try:
        filename = str(last_post.id + 1)
    except:
        filename= "1"

    file = request.files.get("file" )
    title = request.form.get("title")
    content = request.form.get("content") 
    print("----------------------------",title, content, file)

    if file:
        p= "./static/img/posts/"+ filename+".jpg"
        file.save(os.path.join(p))
    upload_post(username,filename,content,title)
    return {}

@app.route('/myaccount', methods=["GET"])
def myaccount_get():
    return render_template("myaccount.html")

@app.route('/myaccount', methods=["POST"])
@token_required
def myaccount(token):
    name= token['username']
    current_user= get_user(name)
    followers= get_followers(name)
    followings= get_followings(name)
    posts= get_posts(name)
    dict= {"posts":[p.id for p in posts[-1::-1]], "followers":followers, "followings":followings, "userid":current_user.id, "err":""}
    dict["ispic"]= os.path.exists(f"static/img/propics/{current_user.id}.jpg")
    return dict

@app.route('/editpost', methods=["POST"])
@token_required
def editpost(token):
    file = request.files.get("file" )
    title = request.form.get("title")
    caption = request.form.get("caption")
    postid = request.form.get("postid")

    post= get_post(postid)
    print("TITLE", title)
    print("CAPTION", caption)
    print("POST-ID: ", postid)
    print("FILE: ", file)
    if post is None or post[0] != token['username']:
        return {}
    p= "./static/img/posts/"+ postid+".jpg"
    if file:
        print("Saving the file")
        file.save(os.path.join(p))
    else:
        try: os.remove(p)
        except: pass
    edit_post(postid,title,caption)
    print("POST EDITED !!")
    return {}
        
@app.route('/deletepost', methods=["POST"])
@token_required
def deletepost(token):
    data = json.loads(request.data)
    postid= data.get("postid", None)
    result = delete_post(postid,token['username'])
    if result: 
        return {}
    else:
        # Change this and display the message "This post cannot be deleted by you" 
        return {}

@app.route('/getpost', methods=["POST"])
def getpost():
    token= request.headers.get('Authentication-Token') 
    if token is not None and token!='null' :
        session['logged_in']= False
        try: token= jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        except: token= None
    else:
        token= None

    data = json.loads(request.data)
    postid = data.get("postid", None)

    post_obj= post.query.filter_by(id=postid).first()
    likes= like.query.filter_by(post=postid).all()
    likes= [l.author for l in likes]
    islike= token['username'] in likes
    obj= {  "author":post_obj.author, "title":post_obj.title, "caption":post_obj.caption, "datetime":post_obj.datetime,
            "ispic": False,
            "islike":islike, "likes":len(likes)}
    return obj


@app.route('/editprofile', methods=["POST"])
@token_required
def editProfile(token):
    data = json.loads(request.data)
    msg = data.get("message", None)
    password = data.get("password", None)
    username= token['username']
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
        res.set_cookie("username",newname, expires="Mon, 01 Jan 2025 00:00:00 GMT")
        welcomeMsg= "Hello! Your username has been changed!"
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
        u_obj.password= generate_password_hash(newpassword)
        # u_obj.password= generate_password_hash(newpassword, method='sha256')

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
@token_required
def upload_profile_pic(token):
    file = request.files.get("file")
    print("File to be uploaded: ", file)
    # id= str(token['username'])
    id= get_user(token['username']).id
    print("id= ", id)
    p= "./static/img/propics/"+ str(id) +".jpg"
    file.save(os.path.join(p))
    return {}

@app.route('/delete_pro_pic', methods=["POST"])
@token_required
def delete_pro_pic(token):
    id= str(get_user(token['username']).id)
    try:
        p= "./static/img/propics/"+ id +".jpg"
        os.remove(p)
        print("REmoveed pic")
    except:
        pass
    return {}

@app.route('/like', methods=["POST"])
@token_required
def like_post(token):
    data = json.loads(request.data)
    postid = data.get("postid", None)
    islike =like.query.filter_by(post=postid, author=token['username']).first()
    if islike:
        print("DISLIKE")
        db.session.delete(islike)
        db.session.commit()
    else:
        l = like(author=token['username'], post=postid)
        print("LIKE")
        db.session.add(l)
        db.session.commit()
    return {}

app.run(port=5000)
