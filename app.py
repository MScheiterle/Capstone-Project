from __init__ import create_app
from config import create_dev_tables

app = create_app()  # For production environment to call

# For development purposes only
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Run app
