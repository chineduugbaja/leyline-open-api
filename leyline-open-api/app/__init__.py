from app.utils import create_app
from app import routes
# Create an instance of the Flask app
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
