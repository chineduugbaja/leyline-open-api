# Leyline Open API

Leyline Open API is a RESTful service that provides domain lookup, IP validation, and query history features. It is designed to run in a Kubernetes environment and supports Docker for containerization. This project uses semantic versioning and is integrated with CI/CD pipelines for automated testing and deployment.

## Features

- **Domain Lookup**: Resolve IPv4 addresses for a given domain.
- **IP Validation**: Validate if an IP address is in IPv4 format.
- **Query History**: Retrieve the latest 20 saved queries.
- **Health Check**: Check the health status of the service.
- **Metrics**: Expose metrics for Prometheus.

## API Endpoints

### `/`

- **GET**: Show current status
  - Returns the current date (UNIX epoch), version, and whether the application is running in Kubernetes.

### `/health`

- **GET**: Show health status
  - Returns the health status of the service.

### `/v1/tools/lookup`

- **GET**: Lookup domain and return all IPv4 addresses
  - **Query Parameter**: `domain` (required)
  - Returns a list of IPv4 addresses for the given domain.

### `/v1/tools/validate`

- **POST**: Simple IP validation
  - **Request Body**: `{ "ip": "<IP_ADDRESS>" }`
  - Returns whether the provided IP is a valid IPv4 address.

### `/v1/history`

- **GET**: List queries
  - Returns the latest 20 saved queries in reverse order (most recent first).

## Development

### Requirements

- Python 3.10+
- Docker
- Docker Compose

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/leyline-open-api.git
   cd leyline-open-api

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt

3. **Run Docker Compose**
    ```bash
    docker-compose up -d --build

## Testing
1. Run Tests Locally.

    ```bash
    pytest

2. Run Tests in CI

Tests are automatically run in the CI pipeline. Ensure your environment is correctly set up with the required secrets.

## Docker
### Dockerfile
The Dockerfile sets up the Python environment, installs dependencies, and defines the entry point for the application.

### Docker Compose
The docker-compose.yml file defines the services required for the application, including the application service and PostgreSQL database.

## Kubernetes
### Helm Chart
A Helm chart is provided to facilitate deployment in a Kubernetes environment. It includes configurations for the deployment, service, ingress, and secrets.

**Deployment**: Deploys the application and sets up replicas.
**Service**: Exposes the application within the Kubernetes cluster.
**Ingress**: Configures ingress rules to access the application externally.
**Secrets**: Stores sensitive information such as database credentials.

### Helm Commands
1. Install or Upgrade

    ```bash
    helm upgrade --install myapp ./helm

2. Uninstall

    ```bash
    helm uninstall myapp

## CI/CD
The CI/CD pipeline is configured with GitHub Actions to:

- Setup a PostgreSQL database
- Run lints and tests
- Build Docker images
- Run Helm lint

## Contact
For questions or feedback, please reach out to cd.ugbaja@gmail.com.