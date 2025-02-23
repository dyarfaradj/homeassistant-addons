# Use Home Assistant Base Image
ARG BUILD_FROM
FROM $BUILD_FROM

# Set up add-on metadata
LABEL \
    org.opencontainers.image.title="Disable Raspberry Pi LEDs" \
    org.opencontainers.image.description="A Home Assistant add-on to disable the Raspberry Pi LEDs dynamically" \
    org.opencontainers.image.vendor="Your Name" \
    org.opencontainers.image.authors="Your Name <your.email@example.com>" \
    org.opencontainers.image.version="1.0"

# Install Python (minimal runtime)
RUN apk add --no-cache python3 py3-pip

# Copy add-on files
COPY control_leds.py /control_leds.py

# Grant execution permissions
RUN chmod +x /control_leds.py

# Run the Python script when the add-on starts
CMD ["python3", "/control_leds.py"]
