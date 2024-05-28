# C2

This is a simple Command-and-Control tool written in Python that communicates over HTTP. The server is a Flask web application, allowing the red teamer to send arbitrary commands to the client and view the results of those commands through a reverse shell, as well as see a list of all connected clients.

## Configuration

## Usage
...
`python3 server.py`

## Limitations
- Unencrypted communication between client and server means that persistence may easily be remediated by blocking the IP of the server.
- Only works with Unix-like operating systems.
