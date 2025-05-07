import socket
import re
import time

# Connection details
HOST = "cyberskills.ch"
PORT = 5004

def solve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    def recv_until_prompt(sock, prompt="Enter a command: "):
        data = b""
        while not data.endswith(prompt.encode()):
            data += sock.recv(1024)
        # print(data.decode(errors='ignore'), end='') # Optional: print server interaction
        return data.decode(errors='ignore')

    def send_command(sock, command):
        # print(command) # Optional: print command sent
        sock.sendall(command.encode() + b"\n")
        time.sleep(0.1) # Give server a moment

    # Initial welcome
    recv_until_prompt(s)

    # 1. Get admin_hash from 'breach'
    send_command(s, "breach")
    breach_output = recv_until_prompt(s)

    # Extract admin hash (e.g., from "{'admin': 'hashvalue', ...}")
    match = re.search(r"'admin': '([0-9a-f]{32})'", breach_output)
    if not match:
        print("Error: Could not find admin hash in breach output.")
        print("Breach output was:")
        print(breach_output)
        s.close()
        return
    admin_hash = match.group(1)
    print(f"[*] Admin hash: {admin_hash}")

    # 2. Construct colliding password
    colliding_password_list = [''] * 32
    initial_xor_val = int('c', 16) # 12

    for k in range(32): # k is the index in our colliding password
        target_hash_idx_affected_by_pk = (k * 13) % 32
        hex_char_to_match = admin_hash[target_hash_idx_affected_by_pk]

        found_char_for_k = False
        for char_code in range(32, 127): # Printable ASCII
            xor_result = char_code ^ initial_xor_val
            produced_hex_char = hex(xor_result)[-1]

            if produced_hex_char == hex_char_to_match:
                colliding_password_list[k] = chr(char_code)
                found_char_for_k = True
                break

        if not found_char_for_k:
            print(f"Error: Could not find char for password index {k} to match hash char {hex_char_to_match} at hash index {target_hash_idx_affected_by_pk}")
            s.close()
            return

    colliding_password = "".join(colliding_password_list)
    print(f"[*] Crafted password: {colliding_password}")
    # print(f"[*] Expected hash for crafted_password: {calculate_hash_local(colliding_password)}") # For local testing

    # 3. Login with "admin" and colliding_password
    send_command(s, "login")
    recv_until_prompt(s, "Enter your username: ")
    send_command(s, "admin")
    recv_until_prompt(s, "Enter your password: ")
    send_command(s, colliding_password)
    login_output = recv_until_prompt(s)

    if "Welcome back, admin!" not in login_output:
        print("[-] Login failed.")
        print("Login output:")
        print(login_output)
        s.close()
        return
    print("[+] Login successful!")

    # 4. Get flag
    send_command(s, "flag")
    flag_output = recv_until_prompt(s)
    print("\n[*] Flag response:")
    print(flag_output) # The flag should be here

    send_command(s, "exit")
    s.close()

if __name__ == "__main__":
    solve()
