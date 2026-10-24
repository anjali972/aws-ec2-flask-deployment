# Production-Style Flask Deployment on AWS EC2

A Flask web application deployed on an AWS EC2 Ubuntu instance using **Nginx as a reverse proxy, Gunicorn as the WSGI application server, and systemd for service management**.

This project demonstrates how to move a Python web application beyond the Flask development server and configure a structured deployment environment on a cloud-based Linux server.

## Project Overview

Deploying a web application involves more than making the application code work. The server must handle incoming requests, forward them to the application, manage the application process, and recover from service failures.

This project implements that deployment flow on AWS EC2.

### Key Objectives

- Deploy a Flask application on an Ubuntu EC2 instance.
- Configure Gunicorn to serve the Flask application.
- Use Nginx as a reverse proxy for incoming HTTP requests.
- Configure systemd to manage the Gunicorn service.
- Restrict direct network access to the application server.
- Organize application dependencies and deployment configuration for maintainability.

## Architecture

![AWS EC2 Flask Deployment Architecture](docs/architecture/architecture.png)

### Request Flow

1. A visitor accesses the website through a browser.
2. The AWS Security Group controls inbound network access.
3. Nginx receives HTTP requests on port `80`.
4. Nginx forwards requests to Gunicorn at `127.0.0.1:8000`.
5. Gunicorn executes the Flask application defined in `app.py`.
6. systemd manages the Gunicorn service and is configured to restart it if it fails.

### Architecture Components

| Component | Responsibility |
|---|---|
| AWS EC2 | Provides the virtual server hosting the application |
| Ubuntu Linux | Operating system for the deployment environment |
| AWS Security Group | Controls inbound network traffic |
| Nginx | Reverse proxy that receives HTTP requests |
| Gunicorn | WSGI server that runs the Flask application |
| Flask | Web application framework |
| systemd | Manages the Gunicorn service lifecycle |
| Python virtual environment | Isolates application dependencies |

## Technology Stack

- **Cloud:** Amazon Web Services (AWS)
- **Compute:** Amazon EC2
- **Operating System:** Ubuntu Linux
- **Backend:** Python, Flask
- **Application Server:** Gunicorn
- **Web Server / Reverse Proxy:** Nginx
- **Service Management:** systemd
- **Version Control:** Git and GitHub

## Repository Structure

```text
aws-ec2-flask-deployment/
├── app.py
├── requirements.txt
├── .gitignore
├── systemd/
│   └── mysite.service
└── docs/
    ├── architecture/
    │   └── architecture.png
    └── screenshots/
        ├── 01-homepage.png
        ├── 02-ec2-instance.png
        ├── 03-security-group.png
        ├── 04-nginx-status.png
        └── 05-gunicorn-status.png
```

The `docs/` directory will contain the architecture diagram and deployment evidence as the documentation is added to the repository.

## Deployment Configuration

### 1. Flask Application

The application is defined in `app.py`. Its Python dependencies are listed in `requirements.txt`, allowing the environment to be recreated without committing the virtual environment itself.

### 2. Gunicorn Application Server

Gunicorn runs the Flask application using the `app:app` application reference and listens on the loopback interface at port `8000`.

Example command:

```bash
gunicorn --workers 2 --bind 127.0.0.1:8000 app:app
```

Binding to `127.0.0.1` keeps Gunicorn accessible locally rather than exposing the application server directly to the public internet.

### 3. Nginx Reverse Proxy

Nginx listens on port `80` and forwards incoming requests to Gunicorn.

This separates public HTTP request handling from application execution and provides a clear boundary between the web server and the Python application.

### 4. systemd Service Management

The `systemd/mysite.service` configuration defines how Gunicorn starts, which user runs it, and the application's working directory.

The service is configured to restart automatically if the process exits unexpectedly.

## Security Considerations

Security is part of the deployment design, not an afterthought.

- **Restricted application port:** Gunicorn listens on `127.0.0.1:8000`, rather than a publicly accessible interface.
- **Network access control:** The EC2 Security Group should permit HTTP traffic on port `80` and restrict SSH access on port `22` to trusted source IP addresses.
- **Secret exclusion:** The `.gitignore` file excludes private key files, environment files, and the Python virtual environment.
- **Dependency management:** Python dependencies are documented in `requirements.txt`.

> **Current limitation:** The website is served over HTTP. HTTPS has not yet been configured. A domain name, TLS certificate, and HTTPS-enabled Nginx configuration can be added as a future improvement.

## Deployment Verification

The deployment can be validated by checking the following:

- The website loads through the EC2 public address.
- Nginx is active and listening for HTTP requests.
- Gunicorn is active under systemd.
- Nginx forwards requests to Gunicorn successfully.
- The application responds successfully to HTTP requests.
- Gunicorn is not directly exposed to the public internet.

Useful diagnostic commands:

```bash
sudo systemctl status nginx --no-pager
```

```bash
sudo systemctl status mysite --no-pager
```

```bash
curl -I http://localhost
```

If the application includes a health endpoint, it can also be checked locally:

```bash
curl http://localhost/health
```

## Deployment Screenshots

Screenshots documenting the deployment will be added here.

### Live Application

![Deployed Flask Website](docs/screenshots/01-homepage.png)

### EC2 Instance

![EC2 Instance Status](docs/screenshots/02-ec2-instance.png)

### Security Group Configuration

![EC2 Security Group Rules](docs/screenshots/03-security-group.png)

### Nginx Status

![Nginx Service Status](docs/screenshots/04-nginx-status.png)

### Gunicorn Status

![Gunicorn Service Status](docs/screenshots/05-gunicorn-status.png)

## Future Improvements

Potential next steps include:

- Configure HTTPS using a TLS certificate and Nginx.
- Connect a custom domain name.
- Configure application and reverse-proxy logging and monitoring.
- Add deployment automation through a CI/CD pipeline.
- Improve operational observability with health checks and resource monitoring.
- Add automated application tests.

## Key Takeaway

This project demonstrates a practical deployment architecture in which the web server, application server, Python application, and service manager have distinct responsibilities.

It provides a foundation for understanding **reverse proxying, WSGI application serving, Linux service management, cloud networking, and deployment security** in an AWS-hosted environment.
