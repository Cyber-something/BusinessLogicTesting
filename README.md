![Image](static/cyberstorelogo_small.png?raw=true&width=50%)
# BusinessLogicTesting | **Crypto Store**
A vulnerable Flask application to enable security professionals to experiment with and assess business logic vulnerabilities.

## Install instructions
```sh
# Install required components
sudo apt update
sudo apt install -y pip git gunicorn

# Get the code of the application
git clone https://github.com/Cyber-something/BusinessLogicTesting.git

cd BusinessLogicTesting

# Install dependencies
pip install -r requirements.txt

# Initialize the application and databse
python3 setup.py

# Start the application in debug mode
python3 app.py

# Run the application with Gunicorn
gunicorn -w 2 --bind localhost:80 wsgi:app
```

### Default credentials
Username: **student**  
Password: **password**