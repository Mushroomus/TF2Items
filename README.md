# TF2Items

## Overview

TF2Items is a Flask application for managing and choosing favourite Team Fortress 2 (TF2) items. 
This guide will help you set up and run the application locally using Docker.

## Prerequisites

- Visual Studio Code or any other IDE of your choice
- Docker installed on your system

## Setup

1. Clone the project repository.
2. Set up environment variables in a `.env` file:
   - `MONGO_CLIENT_URL`: MongoDB connection URL
   - `SECRET_KEY`: Secret key for Flask session management

## Building and Running

1. Open the built-in terminal in your IDE.
2. Build the Docker image:
   ```bash
   docker build -t tf2items-app .
3. Run the Docker container:
    ```bash
    docker container run -d -p 5000:5000 tf2items-app
4. Open the application in your web browser by navigating to: http://127.0.0.1:5000/