import ftplib

def connect_ftp(ip, timeout):
    """
    Attempt to connect to an FTP server at the given IP address.
    """
    try:
        ftp = ftplib.FTP()
        ftp.connect(ip, 21, timeout=timeout)
        ftp.login(user='anonymous', passwd='')
        return ftp
    except Exception as e:
        print(f"FTP connection error: {e}")
        return None

def is_directory(ftp, dir):
    """
    Check if a given item on the FTP server is a directory.
    """
    current = ftp.pwd()
    try:
        ftp.cwd(dir)
        ftp.cwd(current)
        return True
    except ftplib.error_perm:
        return False

def list_files_and_dirs(ftp, path='', indent=''):
    """
    Recursively list the files and directories in the specified path of the FTP server, but only go deeper if there is exactly one directory.
    """
    try:
        contents = []
        ftp.cwd(path)
        items = ftp.nlst()
        dirs = [item for item in items if is_directory(ftp, item)]
        files = [item for item in items if not is_directory(ftp, item)]
        
        for file in files:
            contents.append(f"{indent}{file}")

        for dir in dirs:
            contents.append(f"{indent}{dir}/")
            if len(dirs) == 1:
                subdir_contents = list_files_and_dirs(ftp, dir, indent+'    ')
                contents.extend(subdir_contents)

        ftp.cwd('..')
        return contents
    except Exception as e:
        print(f"Error listing files and directories: {e}")
        return []

def main(timeout_ms):
    """
    Connect to each FTP server in the output file, find the files and directories in the FTP root, and copy them into a file.
    """
    timeout = timeout_ms * 0.001  # Convert milliseconds to seconds
    with open("successful_connections.txt", "r") as infile, open("ftp_contents.txt", "w") as outfile:
        for line in infile:
            ip = line.strip()
            ftp = connect_ftp(ip, timeout)
            if ftp is not None:
                try:
                    contents = list_files_and_dirs(ftp)
                    outfile.write(f"Contents of FTP server at {ip}:\n")
                    outfile.write("\n".join(contents) + "\n\n")
                except Exception as e:
                    print(f"Error scanning FTP server at {ip}: {e}")
                finally:
                    try:
                        ftp.quit()
                    except OSError:
                        pass  # Ignore error if FTP server has timed out
                print(f"Saved files and directories of FTP server at {ip}")

if __name__ == "__main__":
    timeout_ms = float(input("Enter the timeout length in milliseconds: "))
    main(timeout_ms)
