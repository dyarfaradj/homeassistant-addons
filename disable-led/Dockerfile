ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies
RUN apk add --no-cache \
    bash \
    jq

# Copy root filesystem
COPY rootfs /

# Ensure all scripts have execute permissions
RUN chmod a+x /usr/bin/led-control.sh
RUN chmod a+x /run.sh

# Labels
LABEL \
    io.hass.name="Raspberry Pi LED Control" \
    io.hass.description="Control the LEDs on your Raspberry Pi" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="Dyar Faradj <exampler@example.com>"

# Set default command
CMD [ "/run.sh" ]