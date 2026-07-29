# Importing all the stuff I need for this script
import concurrent.futures # this is for multithreading!!
import csv # we need this to save the results as a spreadsheet file later
import socket # needed to talk to the network and internet
import re # regular expressions... this part was hard to learn
from datetime import datetime # to figure out exactly how long my scan took

# Regex to check if the user actually typed a real IP address format
# (I got this pattern from a tutorial, but it basically checks for 4 numbers separated by dots)
ip_add_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")

# Regex to get the lowest and highest port numbers the user types in (like 1-100)
port_range_pattern = re.compile(r"([0-9]+)-([0-9]+)")

def get_banner(s):
    """Try to get a welcome message (banner) from the server we connected to."""
    try:
        # sending a fake HTTP request to trick web servers into talking to us
        s.send(b"HEAD / HTTP/1.1\r\nHost: target\r\n\r\n")

        # receive 1024 bytes of data. 
        # errors="ignore" is super important here so the script doesn't crash on weird binary characters.
        banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
        
        # if we actually got a message back from the server
        if banner:
            # replacing enter keys (newlines) with spaces so it prints nicely on one single line
            return banner.replace("\n", " ").replace("\r", "")
            
    except Exception:
        # if it fails just do nothing
        pass

    # if everything fails, just return this string
    return "No banner detected"

def scan_port(ip, port, timeout=1.0):
    """Connect to a port and see if it is open."""
    try:
        # creating the socket thingy (AF_INET = IPv4, SOCK_STREAM = TCP)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # don't wait forever, timeout after 1 second so the scanner doesn't freeze!
            s.settimeout(timeout)
            # connect_ex is better than regular connect() because it doesn't throw giant errors if the port is closed
            # if it returns 0, it means the 3-way handshake worked perfectly!
            if s.connect_ex((ip, port)) == 0:
                banner = get_banner(s)
                return {"port": port, "status": "Open", "banner": banner}
        
    except Exception:
        pass
    return None # return None if the port is closed or filtered

def save_results(open_ports, filename):
    """Function to save the open ports to a CSV or TXT file on the computer."""
    # check if the user typed .csv at the end of their filename
    if filename.endswith(".csv"):
        # open the file in write mode ('w')
        with open(filename, "w", newline="", encoding="utf-8") as f:
            # setting up the columns for the spreadsheet
            writer = csv.DictWriter(f, fieldnames=["port", "status", "banner"])
            writer.writeheader() # write the column titles at the top
            writer.writerows(open_ports) # dump all my open ports into the file!
    
    else:
        # if it's not a csv, just save it as a normal txt file
        with open(filename, "w", encoding="utf-8") as f:
            # loop through my list and write each one to a new line
            for p in open_ports:
                f.write(f"Port {p['port']} is OPEN: {p['banner']}\n")
                
    # tell the user we finished saving
    print(f"\n[*] Results successfully saved to {filename}")

def main():
    current_year = datetime.now().year # Getting the current year so my copyright is always up to date!

    # My first ASCII text banner attempt. I used https://patorjk.com/software/taag/ to make it.
    print("\n****************************************************************")
    print(r"""
______      _   _                 _____                                 
| ___ \    | | | |               /  ___|                                
| |_/ /   _| |_| |__   ___  _ __ \ `--.  ___ __ _ _ __  _ __   ___ _ __ 
|  __/ | | | __| '_ \ / _ \| '_ \ `--. \/ __/ _` | '_ \| '_ \ / _ \ '__|
| |  | |_| | |_| | | | (_) | | | /\__/ / (_| (_| | | | | | | |  __/ |   
\_|   \__, |\__|_| |_|\___/|_| |_\____/ \___\__,_|_| |_|_| |_|\___|_|   
       __/ |                                                            
      |___/                                                             
      
    """)
    print("\n****************************************************************")
    print(f"\n* Copyright (c) {current_year} [Your Name]. All rights reserved.         *")
    print("\n* Multi-Threaded TCP Port Scanner & Banner Grabber             *")
    print("\n****************************************************************")

    # First, ask user to input the IP address using an infinite loop until they get it right
    while True:
        target_ip = input("\nPlease enter the IP address that you want to scan: ")
    
        # search the input to see if it matches the regex we made at the top
        if ip_add_pattern.search(target_ip):
            print(f"{target_ip} is a valid IP address!\n")
            break # break out of the while loop!
        else:
            print("Invalid IP format! Please use a standard IPv4 address (e.g., 192.168.1.1).")

    # Second, Ask user to input the Port range
    while True:
        print("Please enter the range of ports you want to scan in format: <int>-<int> (ex: 1-1024)")
        port_range = input("Enter port range: ")
    
        # taking away accidental spaces just in case the user typed "1 - 100"
        port_range_valid = port_range_pattern.search(port_range.replace(" ", ""))

        if port_range_valid:
            # group(1) gets the first number, group(2) gets the second number
            port_min = int(port_range_valid.group(1))
            port_max = int(port_range_valid.group(2))
            break
        else:
            print("Invalid port range format! Please try again.\n")

    # Aaesthetic purposes
    print("\n" + "-" * 50)
    print(f"Scanning Target: {target_ip}")
    print("-" * 50)

    # Creating an empty list to hold my open ports later
    open_ports = []
    
    # recording the exact time we started
    start_time = datetime.now()

    # Third,the multi-threaded scanning
    # I used 100 threads to scan multiple ports simultaneously. 
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        # empty list to hold my background tasks
        tasks = []
        # looping from the lowest port to the highest port
        for port in range(port_min, port_max + 1): # (need the +1 otherwise it skips the very last port)
            # sending the scan_port function to a background worker
            task = executor.submit(scan_port, target_ip, port)
            tasks.append(task)

        # check the results as soon as a thread finishes its job
        for future in concurrent.futures.as_completed(tasks):
            result = future.result()
    
            # if result is not None (meaning the port was open!)
            if result:
                # print it out immediately so the user doesn't get bored waiting
                print(f"[+] Port {result['port']} is OPEN | Banner: {result['banner'][:50]}") # [:50] cuts the banner text short so it doesn't mess up my terminal screen
                # save it to my list!
                open_ports.append(result)

    # scan is done!
    print("-" * 50)
    # math to figure out the duration
    print(f"Scan completed in: {datetime.now() - start_time}")
    
    # 4. Optional File Saving
    # if the list actually has stuff in it (length > 0)
    if open_ports:
        # sort the ports from lowest to highest using a weird lambda function 
        open_ports.sort(key=lambda x: x["port"])

        save_choice = input("\nWould you like to save the results to a file? (y/n): ")

        if save_choice.lower() == 'y': # .lower() makes sure it works even if they typed capital 'Y'
            filename = input("Enter filename (e.g., results.txt or results.csv): ")
            save_results(open_ports, filename)
    else:  # if the list was empty
       
        print("\nNo open ports were found. Bummer.")

# this is required in python to make sure main() runs when you double click the script!
if __name__ == "__main__":
    main()