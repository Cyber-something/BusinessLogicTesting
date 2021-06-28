![Image](static/cyberstorelogo_small.png?raw=true)
# BusinessLogicTesting | __Crypto Store__
A vulnerable Flask application to enable security professionals to experiment with and assess business logic vulnerabilities.

## Disclaimer
This is a vulnerable application please do not host this where it can be publicly accessed and exploited.

## Installation instructions
Update and install the required components
```sh
sudo apt update
sudo apt install -y pip git gunicorn
```
Get the application by cloning it from the repo
```sh
git clone https://github.com/Cyber-something/BusinessLogicTesting.git
```

Install all the required dependencies with Pip
```sh
cd BusinessLogicTesting
pip install -r requirements.txt
```

Initialize the application by running setup.py before starting the application. The script can be run afterwards to reset all the contents of the DB 
```sh
python3 setup.py
```

The application can be started in debug mode
```sh
# 125.0.0.1:5000
python3 app.py
```

Alternatively the application can run with Gunicorn as well
```sh
gunicorn -w 2 --bind localhost:5000 wsgi:app
```

### Default credentials
`student:password`