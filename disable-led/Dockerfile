# Use Home Assistant Base Image
ARG BUILD_FROM
FROM $BUILD_FROM

# Install required packages
RUN apk add --no-cache python3 util-linux shadow sudo

# Create directories 
RUN mkdir -p /templates

# Copy files
COPY run.py /
COPY run.sh /
COPY 99-led-permissions.rules /etc/udev/rules.d/

# Make scripts executable
RUN chmod a+x /run.sh /run.py

# Ensure the container has the necessary permissions
RUN echo "root ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Reload udev rules
RUN udevadm control --reload-rules && udevadm trigger

WORKDIR /
CMD [ "/run.sh" ]