from threading import Thread
import socket
from logging import debug, info, warning, error, critical


def udp_to_amx(amx_ip, amx_rx_port=10002, message='test') -> None:
    import sys
    from logging import debug, info, warning, error, critical


    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        error(f'udptoamx udp_to_amx() client socket create {e}')
        sys.exit()

    message = (f"{message}\r").encode()
    client = (amx_ip, amx_rx_port)
    try:
        s.sendto(message, client)
        debug(f"sent {message} to {client}")
    except socket.error as e:
        error(f'udptoamx udp_to_amx() client send socket: {e}')
        sys.exit()
    except Exception as e:
        error(f"djangmx udp_to_amx client send generic: {e}")

    try:
        s.close()
    except socket.error as e:
        error(f'udptoamx udp_to_amx() client socket close {e}')
    # no replies will be received. all rx will be on the server port
    # amx can be too slow to formulate a response and reply in time

    return


class Receiver(Thread):
    def __init__(self,
		sock,
        server_ip,
        server_rx_port,
        django_ip,
        django_port,
	):
        # Call Thread constructor
        super().__init__()
        self.sock = sock
        self.keep_running = True    
        self.server_ip = server_ip
        self.server_rx_port = server_rx_port
        self.django_ip = django_ip
        self.django_port = django_port

    def stop(self):
        # Call this from another thread to stop the receiver
        self.keep_running = False

    def run(self):
        from select import select
        
        # This will run when you call .start method
        while self.keep_running:
            #use select here so that we don't get stuck in recvfrom.
            # wake up every .5 seconds to check whether we should keep running
            rfds, _wfds, _xfds = select([self.sock], [], [], 0.5)
            if self.sock in rfds:
                try:
                    data, addr = self.sock.recvfrom(4096)
                    try:
                        self.rx_data = data.decode()
                    except UnicodeDecodeError as e:
                        error(f"djangmx {self.master_ip} {e}")
                    self.master_ip = addr[0]

                    # amx will never hear this reply since I'm using different rx/tx ports
                    reply = f"ACK\r"
                    self.sock.sendto(reply.encode(), addr)

                    self.parse_rx()
                except socket.error as e:
                    error(f"djangmx Receiver socket {e}")
                    break

    def parse_rx(self):
        import requests
        amx_rx = self.rx_data[:self.rx_data.find('\r')]   # deletes \n
        debug(f'amx_rx: {amx_rx} LENGTH {len(amx_rx)}')

        if 'get_id' in amx_rx:   # request for django ids
            id_url = f"http://{self.django_ip}:{self.django_port}/equipment/get_id/{self.master_ip}"
            info(requests.get(id_url))

        if ":::" in amx_rx:
            # ':::3561~True~Warming Up~Online~123455~:::1234~HDMI1~-45~
            fb_list = amx_rx.split(':::')
            fb_list = fb_list[1::]  #  drop the dead space before the first id
            for fb in fb_list:
                #  3561~True~Warming Up~Online~123455~
                #  1234~HDMI1~-45~
                #  sending the fb data to this url feeds it into django's equipment/urls.py -> amx_fb view
                fb_url = f"http://{self.django_ip}:{self.django_port}/equipment/amx_fb/{fb}"
                info(requests.get(fb_url))


def amx_to_django_listener(server_ip, django_ip, server_rx_port=10004, django_port=8000):
    rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # correct for 'OSError: [Errno 98] Address already in use' when program is restarted
    rx_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    rx_sock.bind((server_ip, server_rx_port))
    info(f"djangmx listening at {server_ip}:{server_rx_port}")
    receiver = Receiver(rx_sock, server_ip, server_rx_port, django_ip, django_port)
    receiver.daemon = True
    receiver.start()
