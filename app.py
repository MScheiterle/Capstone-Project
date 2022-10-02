import os
import pathlib
from __init__ import create_app
from config import create_dev_tables

app = create_app()  # For production environment to call

# For development purposes only
if __name__ == '__main__':
    # Deletes dev db if exists, then remakes it with fresh tables
    print("Starting flask app processes")
    try:
        if not os.path.exists(str(pathlib.Path(
                __file__).parent.resolve()) + f"\\dev.db"):
            print("No database file detected...\n Creating dev.db....")
            create_dev_tables()
            print("dev.db created")
        else:
            print("dev.db exists")
    except FileNotFoundError:
        pass

    print("Running App")
    app.run(host='0.0.0.0', port=5000, debug=True)  # Run app
