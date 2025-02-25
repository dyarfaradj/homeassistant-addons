# Use Home Assistant Base Image
ARG BUILD_FROM
FROM $BUILD_FROM

# Set up add-on metadata
LABEL \
    org.opencontainers.image.title="Raspberry Pi LED Control" \
    org.opencontainers.image.description="A Home Assistant add-on to control the Raspberry Pi LEDs" \
    org.opencontainers.image.vendor="dyarfaradj" \
    org.opencontainers.image.version="1.0.5"

# Install Python
RUN apk add --no-cache python3 util-linux

# Create directories 
RUN mkdir -p /templates

# Copy files
COPY run.py /
COPY run.sh /

# Make scripts executable
RUN chmod a+x /run.sh

WORKDIR /
CMD [ "/run.sh" ]