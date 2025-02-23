FROM ghcr.io/home-assistant/aarch64-base:latest

# Install Python
RUN apk add --no-cache python3 py3-pip

# Copy the Python script
COPY control_leds.py /control_leds.py
RUN chmod +x /control_leds.py

CMD ["python3", "/control_leds.py"]
