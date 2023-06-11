## Basic Requirements: 
You should have Python Installed.  
You should have Linux terminal or WSL activated in case of Windows.  
You should have redis and MailHog installed.  

## Application Setup:
Open Five different terminal windows to run different commands.  
In the terminals, run the following commands:
<<<<<<< HEAD
* Run ` virtualenv projectenv` on ANY of the opened terminals.
* Run `. projectenv/bin/activate`on ALL the opened terminals.
* Run `pip3 install -r requirements.txt` on any of the opened terminals.
* Run `redis-server` to start the redis server on 1st terminal.
* Run `celery -A tasks.celery beat --max-interval 1 -l info` to start the celery beat on 2nd terminal.
* Run `celery -A tasks.celery worker -l info` to start the celery workers on 3rd terminal.
* Run `~/go/bin/MailHog` to connect to MailHog server on 4th terminal.
* Run  `main.py` on 5th terminal.
=======
   * Run ` virtualenv projectenv` on any of the opened terminals
   * Run `. projectenv/bin/activate`on all the opened terminals
* Run `pip3 install -r requirements.txt` on any of the opened terminals
* Run `redis-server` to start the redis server on 1st terminal
* Run `celery -A tasks.celery beat --max-interval 1 -l info` to start the celery beat on 2nd terminal
* Run `celery -A tasks.celery worker -l info` to start the celery workers on 3rd terminal
* Run `~/go/bin/MailHog` to connect to MailHog server on 4th terminal
* Run  `main.py` on 5th terminal  
>>>>>>> 3631c71c1680634385fd38d3cccf69ade213ddeb

It will start the Flask app in development mode. Suited for local development.
    
