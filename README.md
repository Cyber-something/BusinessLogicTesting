# BusinessLogicTesting | **Crypto Store**
A vulnerable Flask application to enable security professionals to experiment with and assess business logic vulnerabilities.

## Install instructions
```bash
git clone https://github.com/Cyber-something/BusinessLogicTesting.git

pip install requirements.txt

python setup.py

python app.py

gunicorn -w 4 --bind localhost:8081 wsgi:app
```