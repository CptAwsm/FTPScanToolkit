import socket
import ftplib
from ipaddress import IPv4Address
import concurrent.futures

def ip_range(start_ip, end_ip):
    """
    Generate a list of IP addresses in the given range.
    """
    start = int(IPv4Address(start_ip))
    end = int(IPv4Address(end_ip))
    return [IPv4Address(ip) for ip in range(start, end+1)]

def check_open_port(ip, port=21, timeout=5):
    """
    Check if the specified port is open on the given IP address.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((str(ip), port))
        sock.close()
        return result == 0
    except:
        return False

def connect_ftp(ip, timeout):
    """
    Attempt to connect to an FTP server at the given IP address.
    """
    try:
        ftp = ftplib.FTP()
        ftp.connect(str(ip), 21, timeout=timeout)
        ftp.login(user='anonymous', passwd='')
        ftp.quit()
        return True
    except Exception as e:
        print(f"FTP connection error: {e}")
        return False

def scan_ip(args):
    """
    Scan a single IP address for an open FTP port and attempt a connection.
    """
    ip, timeout = args
    if check_open_port(ip, 21, timeout):
        if connect_ftp(ip, timeout):
            return str(ip)
    return None

def main(start_ip, end_ip, timeout_ms, threads):
    """
    Scan a range of IP addresses for open FTP ports and attempt connections.
    """
    ip_list = ip_range(start_ip, end_ip)
    total_ips = len(ip_list)
    timeout = timeout_ms * 0.001  # Convert milliseconds to seconds
    successful_connections = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_ip, (ip, timeout)): ip for ip in ip_list}
        for idx, future in enumerate(concurrent.futures.as_completed(futures)):
            ip = futures[future]
            result = future.result()
            if result is not None:
                with open("successful_connections.txt", "a") as outfile:
                    outfile.write(result + "\n")
                print(f"Successful connection to: {result}")
                successful_connections += 1
            print(f"Progress: {idx+1}/{total_ips}, Scanned IP: {ip}, Successful connections: {successful_connections}")

if __name__ == "__main__":
    start_ip = input("Enter the start IP address: ")
    end_ip = input("Enter the end IP address: ")
    timeout_ms = float(input("Enter the timeout length in milliseconds: "))
    threads = int(input("Enter the number of threads: "))
    main(start_ip, end_ip, timeout_ms, threads)
