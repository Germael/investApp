# Docker Image Guide

This README explains how to build, tag, and push a Docker image for deployment on macOS and Ubuntu servers, as well as how to push it to a Docker registry.

## Prerequisites

- **Docker**: Ensure Docker is installed on both your macOS machine and the Ubuntu server.
- **Docker Hub Account** (or other Docker registry): For pushing the image to a remote registry.

---

## Build for macOS

1. Open a terminal and navigate to the directory containing your `Dockerfile`.

2. Build the Docker image for macOS:
   ```bash
   docker build -t invest-app:0.0.1 .
   ```

---

## Build for Ubuntu Server

1. Use the `--platform` flag to build the image for `linux/amd64` (default architecture for Ubuntu servers):
   ```bash
   docker build --platform linux/amd64 -t invest-app:0.0.1 .
   ```

2. Verify the image:
   ```bash
   docker images
   ```
   Expected output:
   ```
   REPOSITORY        TAG       IMAGE ID       CREATED        SIZE
   invest-app     0.0.1     abc123def456   X minutes ago  XYZMB
   ```

## Push Image to Docker Registry

1. **Tag the Image**:
   Replace `username` with your Docker Hub username (or appropriate registry name):
   ```bash
   docker tag invest-app:0.0.1 username/invest-app:0.0.1
   ```

2. **Log in to Docker Hub** (or other registry):
   ```bash
   docker login
   ```
   Enter your credentials when prompted.

3. **Push the Image**:
   ```bash
   docker push username/invest-app:0.0.1
   ```

4. **Pull the Image on Ubuntu Server**:
   On your Ubuntu server, pull the image:
   ```bash
   docker pull username/invest-app:0.0.1
   ```

5. **Run the Container**:
   ```bash
   docker run -d --name my-container-name username/invest-app:0.0.1
   ```

---

## Additional Notes

- **Multi-Platform Builds**: If you need to support multiple architectures, consider using Docker Buildx for multi-platform builds.
- **Environment Variables**: Ensure all required environment variables are set in your `docker-compose.yml` or directly passed to the container.
- **Cleanup**: Remove unused images and containers to free up space:
  ```bash
  docker system prune -af
  ```