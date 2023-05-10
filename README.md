# FTPScanToolkit
2 Python apps to allow easy scanning and listing directories/files within a given IP range for open FTP servers

# ftpscan.py
Run using python 3.6 and above
Give it an ip range, timeout length in ms, and number of threads, it will scan and attempt to connect to each open port 21 as 'anonymous', then list successful connections in a separate file named 'successful_connections.txt' in the same directory.

# ftplist.py
Run using python 3.6 and above
Give it a timeout, and it will check for 'successful_connections.txt" file and connect to each one, listing contents in a text file. It will recurse only if there is 1 directory in the currently scanned directory, otherwise it will save directories and files to a text file named 'ftp_contents.txt'
