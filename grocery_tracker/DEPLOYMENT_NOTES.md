# Deploying the Grocery Tracker App to PythonAnywhere

This guide provides basic steps to deploy the Grocery Tracker Flask application to PythonAnywhere.

## Prerequisites

1.  **A PythonAnywhere Account**: Sign up for a free or paid account at [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/).
2.  **Application Files**: You should have all the application files ready (e.g., by cloning your Git repository or uploading them). This includes:
    *   `app.py`
    *   `wsgi.py`
    *   `requirements.txt`
    *   `templates/` directory (with `index.html`, `edit_item.html`)
    *   `static/` directory (with `style.css`)
    *   (This `DEPLOYMENT_NOTES.md` file)

## Deployment Steps

1.  **Upload Your Files to PythonAnywhere**:
    *   Go to your PythonAnywhere **Dashboard**.
    *   Open a **Bash Console** (or use the "Files" tab to upload files/folders).
    *   Create a directory for your project, e.g., `mkdir ~/my-grocery-app`.
    *   Navigate into it: `cd ~/my-grocery-app`.
    *   Upload your files here. If you use Git, you can clone your repository: `git clone <your-repo-url> .`

2.  **Set up a Virtual Environment (Recommended)**:
    *   In your Bash console, navigate to your project directory (`~/my-grocery-app`).
    *   Create a virtual environment: `python3 -m venv venv` (e.g., using Python 3.9, select your desired Python version available on PythonAnywhere).
    *   Activate it: `source venv/bin/activate`.
    *   Install dependencies: `pip install -r requirements.txt`.

3.  **Configure the Web App on PythonAnywhere**:
    *   Go to the **Web** tab on PythonAnywhere.
    *   Click **Add a new web app**.
    *   Follow the prompts:
        *   Your domain name will be something like `YourUserName.pythonanywhere.com`.
        *   Choose **Manual configuration** (NOT Flask, as we have a wsgi.py).
        *   Select the **Python version** you used for your virtual environment (e.g., Python 3.9). Manual configuration will then show you further instructions.

4.  **Configure WSGI file**:
    *   After creating the web app, you'll be taken to the configuration page for your app.
    *   Scroll down to the **Code** section.
    *   **Source code**: Set this to your project directory, e.g., `/home/YourUserName/my-grocery-app`.
    *   **WSGI configuration file**: Click the link to edit this file. It will likely be something like `/var/www/YourUserName_pythonanywhere_com_wsgi.py`.
        *   **Important**: PythonAnywhere provides a template WSGI file. You need to modify it to point to *your* `wsgi.py` file and application.
        *   Make it look something like this (delete most of the existing template content):

            ```python
            import sys
            import os

            # Path to your project directory (where your wsgi.py and app.py are)
            project_home = u'/home/YourUserName/my-grocery-app' # CHANGE YourUserName and my-grocery-app
            if project_home not in sys.path:
                sys.path.insert(0, project_home)

            # Import your Flask app object from your wsgi.py
            # The 'application' variable is what PythonAnywhere's servers will use
            from wsgi import application # Assumes your wsgi.py has 'application = app'
            ```
        *   Save the file.

5.  **Update Database Path in `app.py`**:
    *   As noted in `app.py`, the `SQLALCHEMY_DATABASE_URI` needs to be an **absolute path** on PythonAnywhere.
    *   Open `app.py` (via the Files tab or a console editor like `nano`).
    *   Change the placeholder path to the actual absolute path where you want your `grocery_inventory.db` file to reside within your PythonAnywhere file storage. For example:
        `app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/YourUserName/my-grocery-app/grocery_inventory.db'`
        (Ensure the directory `/home/YourUserName/my-grocery-app/` exists and is writable by your web app).

6.  **Set up Static Files Mapping (if necessary)**:
    *   On the **Web** tab for your app configuration:
    *   Go to the **Static files** section.
    *   Enter the URL `/static` (or whatever you use in `url_for('static', ...)`).
    *   Enter the corresponding directory path: `/home/YourUserName/my-grocery-app/static`.

7.  **Reload Your Web App**:
    *   Go back to the **Web** tab.
    *   Click the big green **Reload YourUserName.pythonanywhere.com** button.

8.  **Test Your Application**:
    *   Open `http://YourUserName.pythonanywhere.com` in your browser.
    *   Check the **Error log** and **Server log** on the Web tab if you encounter issues.

## Important Notes:

*   **Free Account Limitations**: Free accounts have some limitations (e.g., specific domain name, CPU usage, scheduled tasks run once a day).
*   **Database**: SQLite works on PythonAnywhere but ensure the web app has write permissions to the database file and its directory. For larger applications, consider using PostgreSQL, which PythonAnywhere also supports.
*   **Debugging**: Use the error logs and server logs provided on PythonAnywhere to debug any issues. Print statements in your Flask app often go to the server log.

This guide provides a starting point. Refer to the official PythonAnywhere documentation for more detailed information.
