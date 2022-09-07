import os
import pathlib

from __init__ import create_app
from config import create_dev_tables

app = create_app()  # For production environment to call

# For development purposes only
if __name__ == '__main__':
    # Deletes dev db if exists, then remakes it with fresh tables
    try:
        os.remove(str(pathlib.Path(
            __file__).parent.resolve()) + f"\\dev.db")
    except FileNotFoundError:
        pass
    finally:
        create_dev_tables()

    app.run(host='0.0.0.0', port=5000, debug=True)  # Run app
