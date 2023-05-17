Basic Requirements:
    You should have Python Installed
    You should have Linux terminal or WSL activated in case of Windows.
    You should have celery, redis-server, and MailHog installed

Application Setup:
    Open Five different terminals to run five different servers.
    For each terminal, run the following commands:
        virtualenv env
        . projectenv/bin/activate
    Run tpip3 install -r requirements.tx from any of the opened terminals
    Run redis-server(redis-server) on 1st terminal
    Run celery beat(celery -A tasks.celery beat --max-interval 1 -l info) on 1st terminal
    Run celery worker(celery -A tasks.celery worker -l info) on 1st terminal
    Run MailHog(~/go/bin/MailHog) from opened terminals on 1st terminal
    Run  main.py  on 1st terminal
    It will start the Flask app in development mode. Suited for local development.
