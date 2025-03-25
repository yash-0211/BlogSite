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

celery -A core.tasks.celery worker -l info &
celery -A core.tasks.celery beat --max-interval 1 -l info &

# start flask server
echo "Starting flask server"
python -m core.server
