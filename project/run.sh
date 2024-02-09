if [ -d "projectenv" ]; then
    echo "Activating virtual environment"
    . projectenv/bin/activate
else
    echo "Creating virtual environment"
    virtualenv projectenv
    . projectenv/bin/activate
    pip3 install -r requirements.txt
fi

redis-server &
celery -A tasks.celery worker -l info &
celery -A tasks.celery beat --max-interval 1 -l info &
~/go/bin/MailHog &


# start flask server
echo "Starting flask server"
python main.py
