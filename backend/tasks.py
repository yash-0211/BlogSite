from datetime import datetime, date
from celery.schedules import crontab
from flask import render_template
from schedule_email import send_mail
from workers import celery
from models import user, post, comment, follower


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    print("Adding periodic tasts")
    sender.add_periodic_task(
            crontab(hour=21, minute=43),
            daily_reminder.s(),)
    sender.add_periodic_task(
        crontab(hour=21, minute=43, day_of_month='8', month_of_year='*'),
        monthly_report.s(),)


@celery.task
def daily_reminder():
    print("Sending Daily reminder..")
    allusers = user.query.all()
    today = str(date.today())
    for u in allusers:
        last_post = post.query.order_by(post.id.desc()).first()
        # print(last_post.datetime[:11])
        if last_post is None or last_post.datetime[:11]!=today:
            message= "Hi! This is a reminder that you haven't posted anything today. Please do visit the BlogSite app and post"
            send_mail(receiver=u.email, message=message, subject= "Daily Reminder From BlogSite")
    print("Daily reminder sent ..")


def prevMonth(s): # s="2023-03-24 10:12"
    today = str(date.today())
    return s[:7]== today[:7]

@celery.task
def monthly_report():
    print("Making monthly report..")
    x = datetime.now()
    year = x.year
    month = x.month  
    allusers = user.query.all()
    for u in allusers:
        username= u.username
        posts= post.query.filter_by(author= username).all()
        posts = filter(lambda x: prevMonth(x.datetime) , posts)

        post_titles=[p.title for p in posts ]

        all_comments= comment.query.filter_by(author= username).all()
        all_comments = filter(lambda x: prevMonth(x.datetime) , all_comments)
        comments= []
        for comment in all_comments:
            c_post= post.query.filter_by(id= comment.post).first()
            if c_post.author == u.username:
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

        send_mail(receiver=u.email, message=msghtml, subject= "Monthly Report From BlogSite")
    print("Monthly report sent..")
