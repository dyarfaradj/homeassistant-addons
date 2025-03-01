# Use Home Assistant Base Image
ARG BUILD_FROM
FROM $BUILD_FROM

# Install required packages
RUN apk add --no-cache python3 sudo

# Create directories 
RUN mkdir -p /templates

# Copy files
COPY run.py /
COPY run.sh /

# Make scripts executable
RUN chmod a+x /run.sh /run.py

# Ensure the container has the necessary permissions
RUN echo "root ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

WORKDIR /
CMD [ "/run.sh" ]