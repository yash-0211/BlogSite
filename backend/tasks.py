import json
# from jobs.workers import celery
from datetime import datetime, date
from flask import current_app as app
from models import user, post
from celery import Celery

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import render_template

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS = 'team@bloglite.com'
SENDER_PASSWORD = ''



celery= Celery("My task",  broker="redis://localhost:6379/1" , result_backend="redis://localhost:6379/2")
celery.conf.timezone = 'Asia/Kolkata'
print("tasks.py executing..")

from celery.schedules import crontab

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    print("Adding periodic tasts")
    sender.add_periodic_task(
            crontab(hour=19, minute=45),
            daily_reminder.s(),
            )
    sender.add_periodic_task(
        crontab(hour=22, minute=19, day_of_month='8', month_of_year='*'),
        monthly_report.s(),
            )


@celery.task
def daily_reminder():
    print("Sending Daily reminder..")
    from models import user, post
    allusers = user.query.all()
    today = str(date.today())
    for user in allusers:
        last_post = post.query.order_by(post.id.desc()).first()
        # print(last_post.datetime[:11])
        if last_post is None or last_post.datetime[:11]!=today:
            msg = MIMEMultipart()
            msg['Subject'] = "Daily Reminder"
            msg['From'] = SENDER_ADDRESS
            msg['To'] = user.email
            message= "Hi! This is a reminder that you haven't posted anything today. Please do visit the BlogSite app and post"
            msg.attach(MIMEText(message, 'html'))

            s = smtplib.SMTP(host= SERVER_SMTP_HOST, port= SERVER_SMTP_PORT)
            s.login(SENDER_ADDRESS, SENDER_PASSWORD)
            s.send_message(msg)
            s.quit()
    print("Daily reminder sent ..")


def prevMonth(s): # s="2023-03-24 10:12"
    today = str(date.today())
    return s[:7]== today[:7]

@celery.task
def monthly_report():
    from models import user, post, comment, follower
    print("Making monthly report..")
    x = datetime.now()
    year = x.year
    month = x.month  
    allusers = user.query.all()
    for user in allusers:
        username= user.username
        posts= post.query.filter_by(author= username).all()
        posts = filter(lambda x: prevMonth(x.datetime) , posts)

        post_titles=[post.title for post in posts ]

        all_comments= comment.query.filter_by(author= username).all()
        all_comments = filter(lambda x: prevMonth(x.datetime) , all_comments)
        comments= []
        for comment in all_comments:
            c_post= post.query.filter_by(id= comment.post).first()
            if c_post.author == user.username:
                continue
            comments.append((comment.caption, c_post.title, c_post.author)) #(your_comment, post_title)
        
        followers= follower.query.filter_by(following= username).all()
        followers = filter(lambda x: prevMonth(x.datetime) , followers)
        followers= [follower.person for follower in followers]

        followings= follower.query.filter_by(person= username).all()
        followings = filter(lambda x: prevMonth(x.datetime) , followings)

        followings= [follower.following for follower in followings]
        
        msghtml = render_template("MonthlyReport.html", 
                                  username=username, 
                                  post_titles=post_titles,
                                  comments=comments,
                                  followers=followers,
                                  followings=followings, 
                                  month= date.today().strftime("%B")
                                  )
        msg = MIMEMultipart()
        msg['Subject'] = "Monthly Report"
        msg['From'] = SENDER_ADDRESS
        msg['To'] = user.email
        message= "Hi! This is a reminder that you haven't posted anything today. Please do visit the BlogSite app and post"
        msg.attach(MIMEText(msghtml, 'html'))

        s = smtplib.SMTP(host= SERVER_SMTP_HOST, port= SERVER_SMTP_PORT)
        s.login(SENDER_ADDRESS, SENDER_PASSWORD)
        s.send_message(msg)
        s.quit()
    print("Monthly report sent..")





