import json
import requests
import time
from colorama import init, Fore, Style
import urllib.parse
import random
import string

def get_new_token(query_id):
    # Parse the query_id to get the initData
    init_data = urllib.parse.quote(query_id)

    payload = f"initData={init_data}"  # This is now a URL-encoded string

    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://app.holdcoin.xyz",
        "referer": "https://app.holdcoin.xyz"
    }

    url = "https://api.holdcoin.xyz/miniapps/api/user/telegram_auth"

    for attempt in range(3):
        print(f"\r{Fore.YELLOW + Style.BRIGHT}Mendapatkan token dengan query_id: {query_id}...", end="", flush=True)
        response = requests.post(url, headers=headers, data=payload)
        
        # Check if the response is successful
        if response.status_code == 200:
            try:
                response_json = response.json()
                if response_json and 'data' in response_json:
                    print(f"\r{Fore.GREEN + Style.BRIGHT}Success Created Token", end="", flush=True)
                    return response_json['data'].get('token')  # Return the token if available
                else:
                    print(f"\r{Fore.RED + Style.BRIGHT}Token Not Found: {response_json}", flush=True)
                    break
            except json.JSONDecodeError:
                print(f"\r{Fore.RED + Style.BRIGHT}Response not in JSON format: {response.text}", flush=True)
                break
        else:
            print(f"\r{Fore.RED + Style.BRIGHT}Gagal mendapatkan token, percobaan {attempt + 1}: {response.status_code} {response.text}", flush=True)
            time.sleep(1)  # Wait before the next attempt

    print(f"\r{Fore.RED + Style.BRIGHT}Gagal mendapatkan token setelah 3 percobaan.", flush=True)
    return None

def get_profile(token):
    url = "https://api.holdcoin.xyz/miniapps/api/user/info"
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "Authorization": f"Bearer {token}",  # Assuming token is sent as a Bearer token
        "origin": "https://app.holdcoin.xyz",
        "referer": "https://app.holdcoin.xyz"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        response_json = response.json()
        if response_json['code'] == 0:
            print(f"{Fore.GREEN + Style.BRIGHT}Profile fetched successfully")
            return response_json['data']  # Return the profile data
        else:
            print(f"{Fore.RED + Style.BRIGHT}Error fetching profile: {response_json['msg']}", flush=True)
            return None
    else:
        print(f"{Fore.RED + Style.BRIGHT}Failed to fetch profile, status code: {response.status_code}", flush=True)
        return None
def read_query_ids(filename):
    try:
        with open(filename, 'r') as file:
            query_ids = [line.strip() for line in file if line.strip()]  # Read non-empty lines
            return query_ids
    except FileNotFoundError:
        print(f"{Fore.RED + Style.BRIGHT}File {filename} not found.")
        return []



def get_tasks(token):
    url = "https://api.holdcoin.xyz/miniapps/api/task/lists"
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "Authorization": f"Bearer {token}",
        "origin": "https://app.holdcoin.xyz",
        "referer": "https://app.holdcoin.xyz"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        response_json = response.json()
        if response_json['code'] == 0:
            print(f"{Fore.GREEN + Style.BRIGHT}Tasks fetched successfully")
            return response_json['data']['lists']  # Return the list of tasks
        else:
            print(f"{Fore.RED + Style.BRIGHT}Error fetching tasks: {response_json['msg']}", flush=True)
            return None
    else:
        print(f"{Fore.RED + Style.BRIGHT}Failed to fetch tasks, status code: {response.status_code}", flush=True)
        return None

def finish_task(token, task_id):
    url = f"https://api.holdcoin.xyz/miniapps/api/task/finish_task?id={task_id}"
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "Authorization": f"Bearer {token}",
        "origin": "https://app.holdcoin.xyz",
        "referer": "https://app.holdcoin.xyz"
    }

    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        response_json = response.json()
        if response_json['code'] == 0:
            print(f"{Fore.GREEN + Style.BRIGHT}Task {task_id} finished successfully")
            return response_json['msg']  # Return a success message
        else:
            print(f"{Fore.RED + Style.BRIGHT}Error finishing task: {response_json['msg']}", flush=True)
            return None
    else:
        print(f"{Fore.RED + Style.BRIGHT}Failed to finish task, status code: {response.status_code}", flush=True)
        return None

def generate_random_hash(length=32):
    """Generate a random hash string of a specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def check_coin_storm(token):
    url_get_coin_storm = "https://api.holdcoin.xyz/miniapps/api/user_game_level/getCoinStorm"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "Authorization": f"Bearer {token}",
        "origin": "https://app.holdcoin.xyz",
        "referer": "https://app.holdcoin.xyz"
    }

    response = requests.get(url_get_coin_storm, headers=headers)
    
    if response.status_code == 200:
        response_json = response.json()
        if response_json['code'] == 0:
            if response_json['data'] is None:
                print(f"{Fore.YELLOW}No coins available right now.")
                return None
            else:
                print(f"{Fore.GREEN}Coin storm detected! Collecting coins...")
                return response_json['data']  # Process data if needed
        else:
            print(f"{Fore.RED}Error checking coin storm: {response_json['msg']}")
            return None
    else:
        print(f"{Fore.RED}Failed to check coin storm, status code: {response.status_code}")
        return None

def play_game(token):
    # Check for coin storm
    coin_storm_data = check_coin_storm(token)
    if coin_storm_data is None:
        return  # Exit if no coins available

    # Get the initial collect sequence number from the coin storm data
    collect_seq_no = coin_storm_data.get('collectSeqNo', 1)  # Default to 1 if not available
    collect_amount = 70  # Set your desired collect amount

    # Collect the coins
    new_collect_seq_no = collect_coins(token, collect_amount, collect_seq_no)
    
    # If the collection was successful, update the sequence number for the next collection
    if new_collect_seq_no is not None:
        collect_seq_no = new_collect_seq_no

def collect_coins(token, collect_amount, collect_seq_no):
    url_collect_coin = "https://api.holdcoin.xyz/miniapps/api/user_game/collectCoin"
    hash_code = ""  # Leave hashCode empty if not needed

    payload = f"collectAmount={collect_amount}&hashCode={hash_code}&collectSeqNo={collect_seq_no}"
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "Authorization": f"Bearer {token}",
        "origin": "https://app.holdcoin.xyz",
        "referer": "https://app.holdcoin.xyz"
    }

    print(f"Payload being sent: {payload}")  # Debugging: print the payload

    response = requests.post(url_collect_coin, headers=headers, data=payload)
    
    if response.status_code == 200:
        response_collect_json = response.json()
        if response_collect_json['code'] == 0:
            collected_amount = response_collect_json['data']['collectAmount']
            collect_status = response_collect_json['data']['collectStatus']
            new_collect_seq_no = response_collect_json['data']['collectSeqNo']
            print(f"{Fore.GREEN}Successfully collected {collected_amount} coins. Status: {collect_status}. New sequence number: {new_collect_seq_no}")
            return new_collect_seq_no  # Return the new sequence number
        else:
            print(f"{Fore.RED}Error collecting coins: {response_collect_json['msg']}")
            return None
    else:
        print(f"{Fore.RED}Failed to collect coins, status code: {response.status_code}")
        print(f"Response content: {response.text}")  # Debugging: print the response text
        return None


def main():
    query_ids = read_query_ids("query.txt")

    for query_id in query_ids:
        print(f"{Fore.YELLOW + Style.BRIGHT}Processing query_id: {query_id}...")
        token = get_new_token(query_id)

        if token:
            tasks = get_tasks(token)
            if tasks:
                for task in tasks:
                    if task['isFinish'] == 0:  # Check if the task is not finished
                        finish_task(token, task['id'])  # Finish the task
            
            # After processing tasks, play the game
            #play_game(token)
        else:
            print(f"{Fore.RED + Style.BRIGHT}Failed to get token for query_id: {query_id}")

if __name__ == "__main__":
    main()


