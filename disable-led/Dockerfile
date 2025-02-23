FROM ghcr.io/home-assistant/amd64-base:latest

# Set up the necessary dependencies
RUN apk add --no-cache bash

# Copy the script
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD [ "/run.sh" ]
