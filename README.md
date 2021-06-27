# BusinessLogicTesting | **Crypto Store**
A vulnerable Flask application to enable security professionals to experiment with and assess business logic vulnerabilities.

## Install instructions
```bash
# Install required components
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
gunicorn -w 4 --bind localhost:8081 wsgi:app
```