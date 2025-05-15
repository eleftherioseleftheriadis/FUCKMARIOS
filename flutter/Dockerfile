# Stage 1: Set up the base environment with Flutter
FROM debian:bullseye-slim AS flutter-setup

# Install dependencies
RUN apt-get update && \
    apt-get install -y curl git unzip xz-utils zip libglu1-mesa && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Flutter
ARG FLUTTER_VERSION
ENV FLUTTER_VERSION=3.24.3
RUN curl -o flutter.tar.xz https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_${FLUTTER_VERSION}-stable.tar.xz && \
    tar -xf flutter.tar.xz && \
    mv flutter /opt/flutter && \
    rm flutter.tar.xz

# Configure Git to allow the /opt/flutter directory
RUN git config --global --add safe.directory /opt/flutter

# Update PATH to include Flutter
ENV PATH="/opt/flutter/bin:${PATH}"

# Run Flutter doctor to initialize
RUN flutter doctor

# Stage 2: Create the final image with Flutter pre-installed
FROM flutter-setup AS final

# Set the default working directory
WORKDIR /app

# Verify Flutter installation
RUN flutter --version
