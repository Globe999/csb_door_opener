# CSB Door Opener

This is a Flask application that uses Selenium to automate the process of opening a door at Chalmers studentbostäder. It exposes a single API endpoint `/open` that triggers the door opening process when a GET request is made. It creates a headless browser which executes the same steps as a user would have to do to open a door.

## Environment Variables

The application uses the following environment variables:

- `BASE_URL`: The base URL of the website.
- `LINK_URL`: The URL of the link to be clicked.
- `APTUS_URL`: The URL of the Aptus page.
- `USERNAME`: The username for login.
- `PASSWORD`: The password for login.
- `SECRET_KEY`: The secret key for the Flask application.
- `ENTRANCE_DOOR_ID`: The ID of the entrance door element.
- `PORT`: The port on which the Flask application runs.
- `API_KEY`: The API key for accessing the `/open` endpoint.

Refer to `.env.example` to see default environment variables

## Running the Application

To run the application, first install the required Python packages:

```bash
pip install -r requirements.txt
```

## Docker

The application can also be run inside a Docker container. To build and run the Docker container, use the following docker-compose.yml:

```docker
version: '3'
services:
  csb_door_opener:
    image: globeeee/csb_door_opener:main
    env_file:
      - .env
    ports:
      - "${PORT}:${PORT}"
```
