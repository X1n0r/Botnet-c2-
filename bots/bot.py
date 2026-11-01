import random
import json
import time
from datetime import datetime
from pathlib import Path

BOTS_DIR = Path(__file__).parent.parent / "bots_data"
BOTS_DIR.mkdir(exist_ok=True)
BOTS_FILE = BOTS_DIR / "botnet_bots.json"

def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

def generate_random_location():
    countries = ["US", "DE", "FR", "UK", "NL", "RU", "BR", "IN", "JP", "CA", "AU", "RO"]
    return random.choice(countries)

def generate_random_latency():
    return random.randint(10, 200)

def connect_bot(bot_info):
    time.sleep(random.uniform(0.1, 0.5))
    bot_info["status"] = "online"
    bot_info["connected_at"] = datetime.now().isoformat()
    bot_info["latency"] = generate_random_latency()
    return bot_info

def generate_bots(count):
    bots = []
    print(f"\n[Bot Generator] Generating {count} bots...")
    print("-" * 50)

    for i in range(count):
        ip = generate_random_ip()
        location = generate_random_location()
        bot = {
            "id": i + 1,
            "ip": ip,
            "location": location,
            "status": "connecting",
            "connected_at": None,
            "latency": None
        }

        print(f"[{i+1}/{count}] Generated bot: {ip} ({location})")

        connected_bot = connect_bot(bot)
        bots.append(connected_bot)
        print(f"[{i+1}/{count}] Connected: {ip} - Latency: {connected_bot['latency']}ms")

    print("-" * 50)
    print(f"[Bot Generator] Successfully generated and connected {len(bots)} bots!")
    return bots

def save_bots(bots):
    with open(BOTS_FILE, 'w') as f:
        json.dump(bots, f, indent=2)
    print(f"[Bot Generator] Bots saved to {BOTS_FILE}")

def load_bots():
    if BOTS_FILE.exists():
        with open(BOTS_FILE, 'r') as f:
            return json.load(f)
    return []

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    BOTNET BOT GENERATOR                       ║
    ║                    Creator: ripper.sec                        ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    try:
        count = int(input("Enter number of bots to generate: "))
        if count < 1:
            print("Error: Number must be at least 1")
            return
        if count > 1000:
            print("Warning: Generating more than 1000 bots may take time...")
            confirm = input("Continue? (y/n): ").lower()
            if confirm != 'y':
                return

        bots = generate_bots(count)
        save_bots(bots)

        print("\n[Bot Generator] Botnet Statistics:")
        print(f"  Total Bots: {len(bots)}")
        print(f"  Online Bots: {sum(1 for b in bots if b['status'] == 'online')}")
        print(f"  Locations: {set(b['location'] for b in bots)}")

    except ValueError:
        print("Error: Please enter a valid number")

if __name__ == "__main__":
    main()
