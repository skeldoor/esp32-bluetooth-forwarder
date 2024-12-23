# network_manager.py
import network
import socket
import time

class WiFiManager:
    """
    Manages Wi-Fi connection and starts a simple blocking HTTP server.
    """

    def __init__(self, ssid: str, password: str):
        self.ssid = ssid
        self.password = password

    def connect(self):
        """Connects to Wi-Fi (if not already connected)."""
        wlan = network.WLAN(network.STA_IF)
        if not wlan.isconnected():
            print("Connecting to Wi-Fi...")
            wlan.active(True)
            wlan.connect(self.ssid, self.password)
            while not wlan.isconnected():
                time.sleep(0.5)
        print("Wi-Fi connected:", wlan.ifconfig())
        return wlan.ifconfig()[0]

    def start_http_server(self, generate_metrics_callback):
        """
        Starts a simple blocking HTTP server on port 80.
        Whenever a request arrives, calls `generate_metrics_callback()`
        to get the Prometheus metrics string.
        """
        # Create a socket listening on port 80
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 80))
        s.listen(5)
        print("HTTP server listening on http://0.0.0.0:80")

        # Blocking loop to accept and respond to requests
        while True:
            conn, addr = s.accept()
            try:
                print("Connection from", addr)
                request = conn.recv(1024)  # We won't parse it in detail here

                # Get the current metrics from the callback
                response_body = generate_metrics_callback()
                
                # Build the HTTP response
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/plain; version=0.0.4\r\n"
                    "Connection: close\r\n"
                    "\r\n" +
                    response_body
                )
                conn.sendall(response)
            finally:
                conn.close()
