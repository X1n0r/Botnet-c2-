import socket
import subprocess
import sys
import os
import threading

class TerminalServer:
    def __init__(self, host='0.0.0.0', port=2222):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False

    def start(self):
        """Start the terminal server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True

        print(f"[+] Server listening on {self.host}:{self.port}", flush=True)
        print(f"[+] Connect with PuTTY using Raw mode on port {self.port}", flush=True)
        print(f"[+] Press Ctrl+C to stop the server\n", flush=True)

        try:
            while self.running:
                client_socket, client_address = self.server_socket.accept()
                print(f"[+] New connection from {client_address}")
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("\n[!] Server shutting down...")
        finally:
            self.stop()

    def handle_client(self, client_socket, client_address):
        """Handle individual client connection"""
        try:
            # Send terminal initialization
            client_socket.send(b'\x1b[?25l')  # Hide cursor
            client_socket.send(b'\x1b[2J')   # Clear screen
            client_socket.send(b'\x1b[H')   # Move cursor to top

            # Run main.py with redirected I/O
            main_path = os.path.join(os.path.dirname(__file__), 'main.py')

            # Set environment for colors
            env = os.environ.copy()
            env['TERM'] = 'xterm-256color'
            env['FORCE_COLOR'] = '1'
            env['PYTHONUNBUFFERED'] = '1'

            # Create subprocess
            process = subprocess.Popen(
                [sys.executable, main_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=env,
                text=False,
                bufsize=0
            )

            # Thread to read output
            def read_output():
                try:
                    while True:
                        try:
                            data = process.stdout.read(1024)
                            if not data:
                                break
                            client_socket.send(data)
                        except:
                            break
                except:
                    pass

            # Start output thread
            output_thread = threading.Thread(target=read_output)
            output_thread.daemon = True
            output_thread.start()

            # Read from client and send to process
            try:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    process.stdin.write(data)
                    process.stdin.flush()

                    # Check if process ended
                    if process.poll() is not None:
                        break
            except:
                pass
            finally:
                process.terminate()
                client_socket.close()
                print(f"[-] Connection closed: {client_address}")

        except Exception as e:
            print(f"[!] Error handling client {client_address}: {e}")
            client_socket.close()

    def stop(self):
        """Stop the server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("[!] Server stopped")

if __name__ == "__main__":
    server = TerminalServer(host='0.0.0.0', port=2222)
    server.start()
