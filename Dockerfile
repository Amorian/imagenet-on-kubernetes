# Starting with a slim python container
FROM python:3.7.5-slim

# Document who is responsible for this image
MAINTAINER Alankrith Krishnan "alankrith.krishnan@nyu.edu"

# Expose any ports the app is expecting in the environment
ENV PORT 8080
EXPOSE $PORT

# Set up a working folder and install the pre-reqs
WORKDIR /app
ADD ImageNet/requirements.txt /app
RUN pip3 --no-cache-dir install -r requirements.txt

# Add code as the last Docker layer because it changes the most
ADD ImageNet/imagenet-classes.txt /app/imagenet-classes.txt
ADD ImageNet/main.py  /app/main.py

# Run the service
CMD [ "python", "main.py" ]
