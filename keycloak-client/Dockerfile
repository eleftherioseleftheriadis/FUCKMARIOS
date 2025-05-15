# Stage 1: Build the application with Gradle
ARG gradle_version=jdk22
ARG keycloak_version=25.0.4-debian-12-r0

FROM gradle:${gradle_version} as build

WORKDIR /app

COPY . .

RUN gradle assemble

# Stage 2: Prepare Keycloak with the built application
FROM docker.io/bitnami/keycloak:${keycloak_version}

# Copy the JAR file from the build stage
COPY --from=build /app/build/libs/*.jar /opt/bitnami/keycloak/providers/

# Copy the keystore into the container
COPY server.keystore /opt/bitnami/keycloak/conf/server.keystore
