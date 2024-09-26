from app import app
from wfastcgi import WSGIHandler

# Create the WSGI handler
handler = WSGIHandler(app)

# If this script is executed directly, run the application
if __name__ == "__main__":
    app.run()
