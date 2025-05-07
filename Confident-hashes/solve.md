# Confident Hashes CTF Solution

## 1. Understanding the Vulnerability

The `main.py` script uses a custom hashing function `calculate_hash`:

```python
def calculate_hash(password: str) -> str:
    hash_digest = ['c'] * 32  # Initial hash digest
    i = 0
    for c in password:
        hash_index = i * 13 % 32
        value = int(hash_digest[hash_index], 16) # Current hex value at position
        # New hex value is the last digit of (ASCII of password char XOR current hex value)
        current_hash_value = hex(ord(c) ^ value)[-1]
        hash_digest[hash_index] = current_hash_value
        i += 1
    return ''.join(hash_digest)
```

Key observations:

- The hash digest is always 32 characters long and initialized with `'c'`.
- Each character of the password `password[i]` updates a specific position `hash_index = (i * 13) % 32` in the `hash_digest`.
- The update rule is `hash_digest[hash_index] = hex(ord(password[i]) ^ int(hash_digest[hash_index], 16))[-1]`.
- Since `13` and `32` are coprime, for a password of length 32, each character `password[i]` will map to a unique `hash_index`, effectively setting it once based on its original value of `'c'`.
- The admin's password is very long (2056 characters from `secrets.token_hex(1028)`). While this means many characters overwrite the same `hash_index` slots, the final hash is still a 32-character string.
- The `breach` command thoughtfully publishes the `USER_DATABASE`, including `admin: <admin_hash_value>`.

## 2. The Attack: Crafting a Colliding Password

We can craft a 32-character password that results in the same hash as the admin's password. Let our crafted password be `P_crafted = p_0 p_1 ... p_{31}`.

When `calculate_hash(P_crafted)` is computed:

- The character `p_k` (at index `k` of `P_crafted`) will affect `hash_digest[target_idx]`, where `target_idx = (k * 13) % 32`.
- Since `p_k` is the _only_ character affecting this `target_idx` (for a 32-char password), the original value it's XORed against at `hash_digest[target_idx]` will be `int('c', 16)`.
- So, the resulting character in the hash at `hash_digest[target_idx]` will be `hex(ord(p_k) ^ int('c', 16))[-1]`.

Let `admin_hash` be the hash obtained from the `breach` command.
We want `hex(ord(p_k) ^ int('c', 16))[-1]` to be equal to `admin_hash[target_idx]`.

Algorithm to find `P_crafted`:

1. Initialize `P_crafted = [''] * 32`.
2. Let `initial_xor_base = int('c', 16)`.
3. For each index `k` from `0` to `31` (for characters of `P_crafted`):
   a. Calculate the `target_idx_in_admin_hash = (k * 13) % 32`.
   b. Get the `required_hex_char = admin_hash[target_idx_in_admin_hash]`.
   c. Iterate through printable ASCII characters (e.g., `chr(code)` for `code` from 32 to 126) for `p_k`.
   d. If `hex(ord(p_k) ^ initial_xor_base)[-1] == required_hex_char`, then we've found our character. Set `P_crafted[k] = p_k` and move to the next `k`.
4. Join `P_crafted` to get the final password string.

## 3. Exploitation Script

The following Python script implements this attack:

```python
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
```

To make the script fully runnable for testing, you might want to include a local copy of `calculate_hash` if you uncomment the local check line.

## 4. Running the Exploit

1. Save the script above as `exploit.py` in the `Confident-hashes` directory.
2. Run `python exploit.py`.
3. The script will connect to the server, retrieve the admin's hash, craft the colliding password, log in as admin, and attempt to retrieve the flag.

The flag will be printed to the console.
