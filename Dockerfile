# sPECIFY the original docker image name from the docker hub
FROM debian:stable-slim 


# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive


# Set tthe working directory in the container where we will be working from
WORKDIR /usr/src

# Install Python and pip and MariabDB and update the package list
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev libmariadb-dev mariadb-client

# Copy the requirements.txt file to the working directory in the container
COPY requirements.txt requirements.txt

# # Copy the entrypoint script
COPY entrypoint.sh /usr/local/bin/





# # Make the entrypoint scripts executable
RUN chmod +x /usr/local/bin/entrypoint.sh
# RUN service mariadb start


# Install the python packages from the requirements.txt file
RUN rm /usr/lib/python3.11/EXTERNALLY-MANAGED && \ 
    pip3 install -r requirements.txt

# Copy the app folder to the working directory in the container
COPY . .


# Run the app

# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:application"]
# CMD ["python3", "app.py"]
# ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
# Build the docker image




# Expose the port that the app will be running on
EXPOSE  5000

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
