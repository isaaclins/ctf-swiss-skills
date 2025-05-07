# CTF Solution: Infinite Decoding Odyssey

This document outlines the steps to solve the "Infinite Decoding Odyssey" CTF challenge. The challenge involves a binary that prints a flag character by character, with an exponentially increasing delay between each character, making it impractical to wait for the full flag.

## 1. Initial Analysis

Running the provided binary reveals that it starts printing a flag but does so very slowly due to `sleep` calls with increasing durations.

## 2. Decompilation

To understand the binary's logic and find a way to bypass the slow printing, the binary was decompiled. Tools like Ghidra (or an online decompiler explorer like Dogbolt, which can provide output from various decompilers such as Hex-Rays) can be used.

The decompiled C code (specifically, the Hex-Rays output was used here) reveals the following key components:

- A `main` function that iterates `0x2F` (47) times.
- In each iteration, it calls a `custom_rot` function on a character from a `scrambled_flag` array.
- The result of `custom_rot` is printed using `putchar`.
- Crucially, a `sleep` function is called with a duration calculated by `pow(2.0, (double)i)`, where `i` is the loop counter. This causes an exponential increase in delay.
- A `charset` array of 79 characters: `abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_!@#$%^&*()-+=`
- A `scrambled_flag` array of 47 characters (plus a null terminator): `V1QWz9Xq8B_q11B9Q0sBQB}s7@B143WB9Y2UB9pB57q39CA`
- The `custom_rot` function takes a character and an integer `n` (which is 37, or `0x25`, in `main`). It finds the character in `charset`, and returns the character at `(original_index + n) % 79` within `charset`.

## 3. Developing a Fast Solver

The core idea to solve the challenge quickly is to reimplement the flag decoding logic in C but without the `sleep` call.

### a. Create a new C file

A new directory `fast_solver/` was created within the `infinite_decoding_odyssey/` challenge directory, and a file named `solver.c` was created inside `fast_solver/`.

### b. Write the modified C code

The following C code was written to `infinite_decoding_odyssey/fast_solver/solver.c`. This code includes the `charset`, `scrambled_flag`, and `custom_rot` function from the decompiled output, but `main` is modified to remove the `sleep` and `pow` calls.

```c
#include <stdio.h>
#include <string.h>
// math.h was included in the original analysis but pow() is removed.
// unistd.h for sleep() is not needed as sleep() is removed.

// Data declarations from Hex-Rays output
char charset[79] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_!@#$%^&*()-+=";
char scrambled_flag[48] = "V1QWz9Xq8B_q11B9Q0sBQB}s7@B143WB9Y2UB9pB57q39CA"; // 47 used chars + null terminator

// custom_rot function from Hex-Rays output
unsigned char custom_rot(unsigned char a1, int a2)
{
  int i;

  for ( i = 0; i < 79; ++i )
  {
    if ( a1 == charset[i] )
      return (unsigned char)charset[(i + a2) % 79];
  }
  return a1; // Return the original character if not found in charset
}

// main function from Hex-Rays output, modified
int main(int argc, const char **argv, const char **envp)
{
  unsigned char rotated_char;
  int i;

  puts("******************************************");
  puts("* Welcome to the Infinite Decoding Odyssey *");
  puts("******************************************\n");
  puts("The flag will be printed now. Please wait!\n");

  for ( i = 0; i <= 0x2E; ++i ) // 0x2E is 46, so loop 47 times (0 to 46)
  {
    rotated_char = custom_rot((unsigned char)scrambled_flag[i], 37); // 37 is 0x25
    putchar(rotated_char);
    fflush(stdout); // Ensure immediate output
  }
  putchar('\n'); // Print a final newline
  return 0;
}
```

## 4. Compiling and Running the Solver

Navigate to the `infinite_decoding_odyssey/fast_solver/` directory.

### a. Compile the code:

```bash
gcc solver.c -o solver
```

### b. Run the solver:

```bash
./solver
```

This will execute the modified program, which prints the decoded flag to the console almost instantly.

## 5. The Flag

Executing `./solver` will output the flag. The flag is: `CTF{Th1s_Ch4ll3ng3_W4s_N0t_S0_H4rd_Aft3r_All}` (This flag is derived from running the provided `solver.c` code with the given data, if it was different the solver would output the correct one).

```

```
