# Install

    virtualenv venv
    source venv/bin/activate

    pip install -r requirements-dev.txt

You need to add copy default config and change facebook related settings
(token and app_id):

    cp project/settings/local{_template,}.py

Create database to store users and external account connections:

    python create_db.py

# Run

    python app.py

# Tests

    nosetests