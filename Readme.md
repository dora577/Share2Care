# Share2Care

## About Project
The project is called Share2Care, and its main aim is to connect people to divide and buy smaller portions of multi-package products. The SQL instance is deployed on GCP (Google Cloud Platform).

### Information about team and project summary is on the [TeamInfo file](TeamInfo.md).
### [Demo Video Link](https://drive.google.com/file/d/1-kaGQHDEymfJVNZQxzXD05s7iYzvPcnG/view?usp=sharing)

## Setup

### Pre-requisites
You need to have a MySQL instance installed either on a remote server or locally.

### Installation
Run the following command to install the required Python packages:

```bash
pip install -r requirements.txt
```

## Run

### Running Locally

1. **Set up the virtual environment** (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set environment variables for development**:

    ```bash
    export FLASK_APP=your_application_name  # Replace `your_application_name` with the name of your Flask app's main module
    export FLASK_ENV=development  # This enables debug mode
    ```

4. **Run the Flask app**:

    ```bash
    flask run
    ```

### Running on Google Cloud

1. **Install the Google Cloud SDK** if you haven't already:

    ```bash
    curl https://sdk.cloud.google.com | bash
    exec -l $SHELL
    gcloud init
    ```

2. **Authenticate and set up your project**:

    ```bash
    gcloud auth login
    gcloud config set project [YOUR_PROJECT_ID]  # Replace with your Google Cloud project ID
    ```

3. **Deploy your app**:

    ```bash
    gcloud app deploy
    ```

4. **Visit your deployed app**:

    ```bash
    gcloud app browse
    ```

By following these steps, you should be able to run and deploy your Flask application both locally and on Google Cloud Platform.
