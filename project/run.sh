if [ -d "projectenv" ]; then
    echo "Activating virtual environment"
    . projectenv/bin/activate
else
    echo "Creating virtual environment"
    virtualenv projectenv
    . projectenv/bin/activate
    pip3 install -r requirements.txt
fi

# start flask server
echo "Starting flask server"
python main.py
