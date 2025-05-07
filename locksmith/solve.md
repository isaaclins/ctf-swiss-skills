# Locksmith CTF Solution Guide

This document will guide you through solving the Locksmith CTF challenge.

## Initial Setup: Running the Executable in Docker

The `locksmith` file is a Linux executable. To run it on your macOS system, we will use Docker.

### Steps:

1.  **Ensure Docker is Installed and Running**:
    If you don't have Docker, download and install it from [Docker's official website](https://www.docker.com/products/docker-desktop/). Make sure the Docker daemon is running.

2.  **Open Your Terminal**.

3.  **Navigate to the CTF directory**:
    Make sure your terminal's current working directory is `ctf-swiss-skills`. If you are in the workspace root, you are already there.

    ```bash
    cd /Users/isaaclins/Documents/github/ctf-swiss-skills
    ```

4.  **Run the Locksmith Executable in an Ubuntu Docker Container**:
    To run the `locksmith` executable, we need to mount it into a Docker container. The key is to correctly specify the path to your `locksmith` file(s) on your host machine for the Docker volume mount (`-v`).

    The error `chmod: cannot access '/mnt/ctf/locksmith': Not a directory` typically occurs if the path inside the Docker command doesn't correctly point to the executable _within the mounted volume_. This can happen if you mount a file directly to a path (e.g., `/mnt/ctf`) and then try to access a subpath (e.g., `/mnt/ctf/locksmith`).

    Here are two ways to run the command:

    **Option 4.1: Using an Absolute Path (Recommended for Reliability)**
    This method mounts your local **directory** `/Users/isaaclins/Documents/github/ctf-swiss-skills/locksmith` (which contains the `locksmith` executable) to `/mnt/ctf` inside the Docker container. The executable will then be accessible at `/mnt/ctf/locksmith` within the container. This command works regardless of your current terminal directory.

    Copy and paste the following command into your terminal:

    ```bash
    docker run --rm -it -v "/Users/isaaclins/Documents/github/ctf-swiss-skills/locksmith":/mnt/ctf ubuntu:latest /bin/bash -c "chmod +x /mnt/ctf/locksmith && /mnt/ctf/locksmith"
    ```

    **Troubleshooting: Rosetta Error on Apple Silicon (M1/M2/M3 Macs)**
    If you are using an Apple Silicon Mac and encounter an error like `rosetta error: failed to open elf at /lib64/ld-linux-x86-64.so.2`, it means Rosetta 2 (Apple's x86_64 emulator) is having trouble running the x86_64 Linux binary inside the container. To resolve this, you can explicitly tell Docker to use an `amd64` (x86_64) version of the Ubuntu image by adding the `--platform linux/amd64` flag:

    **Corrected command for Apple Silicon:**

    ```bash
    docker run --rm -it --platform linux/amd64 -v "/Users/isaaclins/Documents/github/ctf-swiss-skills/locksmith":/mnt/ctf ubuntu:latest /bin/bash -c "chmod +x /mnt/ctf/locksmith && /mnt/ctf/locksmith"
    ```

    **Option 4.2: Using a Relative Path (Requires Correct Current Working Directory)**
    If you prefer to use a relative path, you **must first ensure your terminal's current working directory is `ctf-swiss-skills`** (i.e., the parent directory of your `locksmith` folder). If you are in `/Users/isaaclins/Documents/github/ctf-swiss-skills`, then `$(pwd)/locksmith` correctly refers to the `locksmith` _directory_.

    If your current directory is `/Users/isaaclins/Documents/github/ctf-swiss-skills`, you can run:

    ```bash
    docker run --rm -it -v "$(pwd)/locksmith":/mnt/ctf ubuntu:latest /bin/bash -c "chmod +x /mnt/ctf/locksmith && /mnt/ctf/locksmith"
    ```

    If you're on Apple Silicon and using this relative path method, you'd add the platform flag here too:

    ```bash
    docker run --rm -it --platform linux/amd64 -v "$(pwd)/locksmith":/mnt/ctf ubuntu:latest /bin/bash -c "chmod +x /mnt/ctf/locksmith && /mnt/ctf/locksmith"
    ```

    If your current directory was `.../locksmith` (the one containing the executable) and you used `$(pwd)/locksmith` in the `-v` mapping to `/mnt/ctf`, this would map the _file_ directly to `/mnt/ctf`, causing issues with the subsequent `chmod /mnt/ctf/locksmith` command.

    **Breakdown of the Docker command:**

    - `docker run --rm -it`: Runs a new container. `--rm` removes the container when it exits. `-it` provides an interactive terminal.
    - `-v "HOST_DIRECTORY_PATH":CONTAINER_DIRECTORY_PATH`: Mounts the `HOST_DIRECTORY_PATH` (containing your `locksmith` executable) to `CONTAINER_DIRECTORY_PATH` (e.g. `/mnt/ctf`) inside the container.
    - `ubuntu:latest`: Specifies the Docker image to use (latest Ubuntu).
    - `/bin/bash -c "chmod +x /mnt/ctf/locksmith && /mnt/ctf/locksmith"`: The command to run inside the container. It first makes the `locksmith` file (located at `/mnt/ctf/locksmith` within the container) executable and then runs it.

5.  **Observe the Output**:
    The program should now run inside the Docker container. Note down any output, prompts, or errors it produces. This will be crucial for the next steps in solving the crypto challenge.

    Expected Output (if running on Apple Silicon with the `--platform` flag, or natively on an x86-64 Linux system):

    ```
    Decrypted password for this minute: NhbEhhZhdvhoEdwSdggohilvkCheudFurfrgloh
    Time remaining until password change: 58 seconds
    Please enter the password:
    ```

    _(The exact password string and time remaining may vary each time you run it.)_

## Step 2: Entering the Provided Password

The program provides a string it calls the "Decrypted password for this minute" and then prompts for a password. The most direct approach is to use this provided string.

1.  When the program outputs the "Decrypted password" and prompts you to "Please enter the password:", copy the password string it provided.
    For example, if it outputs: `Decrypted password for this minute: YourUniqueGeneratedPasswordString`

2.  **Quickly** paste this string (`YourUniqueGeneratedPasswordString` in the example, or `NhbEhhZhdvhoEdwSdggohilvkCheudFurfrgloh` from our current run) into the terminal where the Docker container is waiting for input, and press Enter.

3.  Observe and record the program's response. This will tell us if the password was correct and what the next step (if any) is.

    If you entered the initially provided string (e.g., `NhbEhhZhdvhoEdwSdggohilvkCheudFurfrgloh`) and it failed, you might see:

    ```
    Password is incorrect. The key is playing hide and seek with the animals. Give it another try!
    ```

## Step 3: Decrypting the Provided String (Caesar Cipher)

The clue "The key is playing hide and seek with the animals" combined with the structure of the provided string (e.g., `NhbEhhZhdvhoEdwSdggohilvkCheudFurfrgloh`) suggests that this string is actually _encrypted_, and we need to decrypt it to find the true password.

**Analysis of the example string `NhbEhhZhdvhoEdwSdggohilvkCheudFurfrgloh`:**

Observing this string, and considering the "animals" clue, parts of it resemble animal names if subjected to a Caesar cipher shift.

If we apply a Caesar cipher shift of **-3 (or +23)**, preserving case:

Original: `N h b E h h Z h d v h o E d w S d g g o h i l v k C h e u d F u r f r g l o h`
Shift -3: `K e y B e e W e a s e l B a t P a d d o c k f i s h Z e b r a C r o c o d i l e`

The decrypted string appears to be `KeyBeeWeaselBatPaddockfishZebraCrocodile`.

This indicates the program is giving us a Caesar-encrypted string (with a shift of +3 from plaintext to ciphertext, or -3 from ciphertext to plaintext), and the decrypted plaintext is likely the password.

**Action Plan:**

1.  Run the `locksmith` executable in Docker again. It will provide a new string for "Decrypted password for this minute".
    ```bash
    docker run --rm -it --platform linux/amd64 -v "/Users/isaaclins/Documents/github/ctf-swiss-skills/locksmith":/mnt/ctf ubuntu:latest /bin/bash -c "chmod +x /mnt/ctf/locksmith && /mnt/ctf/locksmith"
    ```
2.  Copy the new string provided by the program.

3.  **Use the `caesar_cracker.py` script to decrypt the string:**
    We have created a helper script `locksmith/caesar_cracker.py` to automate finding the correct decryption.

    a. Open a new local terminal window/tab (separate from the Docker one).
    b. Navigate to the `locksmith` directory in your project:
    `bash
cd /Users/isaaclins/Documents/github/ctf-swiss-skills/locksmith
`
    c. Run the script with the new ciphertext string as an argument. For example, if the program gave you `YourCiphertextGoesHere`, you would run:
    `bash
python caesar_cracker.py "YourCiphertextGoesHere"
`
    d. The script will output all 25 possible Caesar decryptions. Our hypothesis is that the program uses a Caesar cipher with a +3 shift (encrypting) or -3 shift (decrypting).
    Look for the line in the script's output that says:
    `Undoing shift +03 (or trying key -03): THE_DECRYPTED_PASSWORD_STRING`
    This `THE_DECRYPTED_PASSWORD_STRING` is what we need.

4.  Enter the `THE_DECRYPTED_PASSWORD_STRING` (obtained from the script for shift +03) as the password into the `locksmith` program's prompt (in the Docker terminal).

5.  Observe the output. If it's successful, we might get the flag or the next part of the challenge!

---

_(We will update this guide as we discover more about the challenge.)_
