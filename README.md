# BlogSite
BlogSite is a web application that allows users to upload blog posts. The user can search for other users and follow them to have their latest posts visible on their feed.  
The user has the CRUD on their posts and can like and comment on any post.  
The user can export data as CSV, change their username/email/password, or delete their account permanently.  
The data displayed on the web page are cached for 10 seconds.  
The user gets daily reminder emails if they do not upload any post and also gets a monthly report about their activity via mail.  

**Technology Used**: 
- Flask for Backend   
- Bootstrap for styling and VueJs, Vue CLI and Vue router for Frontend    
- PostgresQL for database  
- Redis for Caching  
- MailHog for the fake SMTP server to send emails.  
- Linux shell (or WSL in the case of Windows)  
