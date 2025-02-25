# Use Home Assistant Base Image
ARG BUILD_FROM
FROM $BUILD_FROM

# Set up add-on metadata
LABEL \
    org.opencontainers.image.title="Raspberry Pi LED Control" \
    org.opencontainers.image.description="A Home Assistant add-on to control the Raspberry Pi LEDs" \
    org.opencontainers.image.vendor="dyarfaradj" \
    org.opencontainers.image.version="1.0.4"

# Install Python
RUN apk add --no-cache python3

# Create directories 
RUN mkdir -p /templates

# Copy files
COPY run.py /run.py

# Make executable
RUN chmod +x /run.py

# Run the app
CMD ["python3", "/run.py"]