ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    jq

# Install Python packages
RUN pip3 install --no-cache-dir \
    requests \
    schedule

# Copy root filesystem
COPY rootfs /

# Ensure run script has execute permissions
RUN chmod a+x /run.py

# Labels
LABEL \
    io.hass.name="LG Dev Session Auto Renew" \
    io.hass.description="Automatically calls an LG Developer URL to renew Developer Mode sessions on your LG webOS TV" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="dyarfaradj <dyarfaradj@example.com>"

# Set default command
CMD [ "python3", "/run.py" ]
