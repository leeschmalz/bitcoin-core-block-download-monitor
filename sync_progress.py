import time
import subprocess
import json
from datetime import datetime

def get_blockchain_info():
    result = subprocess.run(['./src/bitcoin-cli', 'getblockchaininfo'], capture_output=True, text=True)
    return json.loads(result.stdout)

def log_progress():
    last_block_count = 0
    last_time = time.time()
    first = True
    while True:
        blockchain_info = get_blockchain_info()
        current_blocks = blockchain_info["blocks"]
        total_headers = blockchain_info["headers"]
        verification_progress = blockchain_info["verificationprogress"]
        
        percent_complete_by_blocks = (current_blocks / total_headers) * 100
        percent_complete_verification = verification_progress * 100

        current_time = time.time()
        elapsed_time = current_time - last_time
        blocks_synced = current_blocks - last_block_count
        syncing_rate = blocks_synced / elapsed_time if elapsed_time > 0 else 0
        if not first:
            print(f"Update Time: {datetime.now().hour}:{datetime.now().minute}")
            print(f"Current Block: {current_blocks}")
            print(f"Total Blocks: {total_headers}")
            print("")
            print(f"Synced {blocks_synced} in {round(elapsed_time/60,2)} mins")
            print(f"Rate: {syncing_rate:.2f} blocks/s")
            print(f"Progress by Block Count: {percent_complete_by_blocks:.2f}%")
            print(f"Progress by Core Report: {percent_complete_verification:.2f}%")
            print("")
            print("=" * 60)
            print("")
        first = False
        last_block_count = current_blocks
        last_time = current_time

        time.sleep(60*5)  # Wait for 5 mins before the next update

if __name__ == "__main__":
    log_progress()
