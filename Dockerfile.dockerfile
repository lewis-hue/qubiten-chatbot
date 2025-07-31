# Use an official Python runtime as a parent image.
# This base image is suitable for Cloud Run deployments.
FROM python:3.9-slim-buster

# Set the working directory inside the container.
# All subsequent commands will run from this directory within the container.
WORKDIR /app

# Copy the requirements.txt file into the container.
# This step is done before copying the rest of the application code to leverage Docker's layer caching.
# If only requirements.txt changes, pip install won't re-run.
COPY requirements.txt .

# Install any needed Python packages.
# --no-cache-dir: Prevents pip from storing cache, reducing image size.
# -r requirements.txt: Installs packages listed in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Flask application code into the container.
# This includes your app.py and any other source files.
COPY . .

# Expose the port your Flask app will run on.
# Cloud Run services typically expect applications to listen on port 8080.
# This environment variable tells your Gunicorn server which port to bind to.
ENV PORT 8080

# Define the command to run your application using Gunicorn.
# Gunicorn is a production-ready WSGI server for Flask.
# `CMD exec gunicorn --bind 0.0.0.0:$PORT app:app` means:
# - `exec`: Ensures signals (like termination signals from Cloud Run) are properly handled.
# - `--bind 0.0.0.0:$PORT`: Tells Gunicorn to listen on all network interfaces on the specified port (8080).
# - `app:app`: Specifies that your Flask application instance named 'app' is found within the 'app.py' file.

# --- How to use this Dockerfile with Google Cloud Console ---
# 1. Store this Dockerfile and your application files (app.py, requirements.txt)
#    in a Cloud Source Repository (or GitHub/Bitbucket/GitLab connected to Cloud Build).
# 2. In the Google Cloud Console, navigate to "Cloud Build" -> "Triggers".
# 3. Click "Create trigger".
# 4. Configure the trigger:
#    - Name your trigger.
#    - Select your source repository.
#    - Choose "Dockerfile" as the build type.
#    - Specify the Dockerfile path (usually `/Dockerfile`).
#    - Specify the image name. For Artifact Registry, it's `REGION-docker.pkg.dev/PROJECT_ID/REPO_NAME/IMAGE_NAME`.
#      Example: `us-central1-docker.pkg.dev/your-gcp-project-id/qa-app-repo/qa-backend-flask`
#    - Set the tag (e.g., `latest`).
# 5. Run the trigger manually or set it to run on commits.
#    Cloud Build will use this Dockerfile to build your container image and push it to Artifact Registry.
# 6. Once the image is built, navigate to "Cloud Run" in the Google Cloud Console.
# 7. Click "Create Service" or select an existing service to revise.
# 8. Select your newly built container image from Artifact Registry.
# 9. Configure service settings (region, memory, CPU, autoscaling, environment variables, service account).
#    Ensure the service account has the `Vertex AI User` role to call your model.
# 10. Click "Deploy".
CMD exec gunicorn --bind 0.0.0.0:$PORT app:app
