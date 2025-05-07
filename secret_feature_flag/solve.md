# CTF Solution: secret_feature_flag

## 1. Challenge Overview

The challenge `secret_feature_flag` involves a Linux executable that presents a menu for a "Cyberpunk Cybernetic Implants Shop". The goal is to uncover a hidden feature to reveal the flag.

**Files:**

- `secret_feature_flag`: An ELF 64-bit LSB pie executable for x86-64 Linux.
- `secret_feature_flag.txt`: A text file appearing to be a hex dump or containing sections of the binary. Key strings like `secret_feature_flag.c`, function names (`getenv`, `read_the_flag`), and the strings `MENU_ACCESS` and `show_hidden` were found within.

## 2. Key Discovery: Environment Variable

Analysis of the binary's strings (using the `strings` command) revealed that the program likely checks for an environment variable named `MENU_ACCESS`. Setting this variable to `show_hidden` is expected to unlock a "Secret Augmentation" menu option, which in turn calls a function to display the flag.

## 3. Solution Steps

### a. Setup Docker Environment

Since the binary is for Linux, a Docker environment is required to run it on macOS.

1.  **Get Absolute Path**: On your macOS terminal, navigate to the `secret_feature_flag` directory and run `pwd` to get its absolute path.
2.  **Run Docker Container**:
    ```bash
    # Replace YOUR_ABSOLUTE_PATH_HERE with the path obtained in the previous step
    docker run -it \
        --platform linux/amd64 \
        --privileged \
        --name sff_env \
        -v YOUR_ABSOLUTE_PATH_HERE:/mnt/ctf \
        ubuntu bash
    ```
    - `--platform linux/amd64` is important for Apple Silicon Macs. Intel Macs might not need it.
    - `--privileged` can be helpful for debugging tools if needed later.
    - `-v` mounts your local CTF directory into `/mnt/ctf` inside the container.

### b. Execute the Binary with the Secret Flag

1.  **Navigate and Prepare**: Inside the Docker container's shell:

    ```bash
    cd /mnt/ctf
    chmod +x ./secret_feature_flag
    ```

2.  **Run with Environment Variable**: Execute the program, setting the `MENU_ACCESS` environment variable:

    ```bash
    MENU_ACCESS=show_hidden ./secret_feature_flag
    ```

3.  **Access Secret Feature and Get Flag**:
    - The program will display its menu. You should now see an additional option:
      ```
      Welcome to the Cyberpunk Cybernetic Implants Shop!
      1. Neural Enhancer
      2. Bionic Arm
      3. Retinal Display
      4. Exit
      5. Secret Augmentation
      Please select an option:
      ```
    - Enter `5` and press Enter.
    - The program will then print a message including the flag:
      ```
      You discovered the Secret Augmentation!
      You can now read somebody else's thoughts, but only once per day.
      You use it on an organizer to get a flag: FLAG{...example_flag_format...}
      ```
      (The actual flag will be displayed here).

## 4. Troubleshooting (If the above doesn't work as expected)

If setting `MENU_ACCESS=show_hidden` and selecting option 5 does not immediately yield the flag:

- **Verify Environment Variable**:
  - Inside Docker, try: `export MENU_ACCESS=show_hidden` then `./secret_feature_flag`.
- **Alternative Values**: Try other common boolean values for `MENU_ACCESS`:
  - `MENU_ACCESS=true ./secret_feature_flag`
  - `MENU_ACCESS=1 ./secret_feature_flag`
- **Use `ltrace`**: This tool can show library calls, including `getenv`.
  ```bash
  # Install if not present: apt update && apt install -y ltrace
  ltrace -e getenv ./secret_feature_flag
  # or when running with the variable:
  # MENU_ACCESS=some_value ltrace -e getenv ./secret_feature_flag
  ```
  This will show if `getenv("MENU_ACCESS")` is being called and what its return value is. It might also reveal if a different variable name is being checked.
- **Use `strace`**: For system call tracing.
  ```bash
  # Install if not present: apt update && apt install -y strace
  strace -e execve,getenv ./secret_feature_flag
  ```
- **Debugging with GDB**: For deeper inspection if other methods fail.
  - `apt install -y gdb`
  - `gdb ./secret_feature_flag`
  - Set breakpoints (e.g., `b main`, `b read_the_flag`, `b strcmp`, `b getenv`).
  - `run` (or `r`) the program.
  - Step through code (`n` for next, `s` for step into) and inspect variables (`p variable_name`) or registers (`info registers`).

This refined `solve.md` should serve as clear documentation for obtaining the flag.
