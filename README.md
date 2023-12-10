# BlogSite
BlogSite is a web application that allows users to add blog posts. The user can search for other users and follow them to have their latest posts visible on their feed.  
The user has the CRUD on their posts and can add/delete comments on any posts.  
The user can export data as CSV, change their username/email/password, or delete their account permanently.  
The data displayed on the web page are cached for 10 seconds.  
The user gets daily reminder emails if they do not make any posts and also gets a monthly report about their activity via mail.  

**Technology Used**: 
- Flask for Backend   
- HTML/CSS/Bootstrap/VueJs for Frontend  
- Sqlite for database.  
- Redis for Caching  
- MailHog for the fake SMTP server to send emails.  
- Linux shell (or WSL in the case of Windows)  
