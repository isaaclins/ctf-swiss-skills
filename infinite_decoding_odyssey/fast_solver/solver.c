#include <stdio.h>
#include <string.h>
#include <math.h> // Included for completeness, though pow() is removed.
// sleep() is removed, so unistd.h is not strictly needed for it.

// Data declarations from Hex-Rays output
char charset[79] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_!@#$%^&*()-+=";
char scrambled_flag[48] = "V1QWz9Xq8B_q11B9Q0sBQB}s7@B143WB9Y2UB9pB57q39CA"; // 47 used chars + null terminator

// custom_rot function from Hex-Rays output
// (Using unsigned char for return to match putchar more directly, and for parameter a1)
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
  unsigned char rotated_char; // Changed type to unsigned char
  int i;

  // Original puts calls for context, can be kept or removed
  puts("******************************************");
  puts("* Welcome to the Infinite Decoding Odyssey *");
  puts("******************************************\n"); // Original had \n, keeping as is.
  puts("The flag will be printed now. Please wait!\n"); // Original had \n

  // Loop directly for 0x2E (46) iterations, which is 0 to 46 inclusive.
  // scrambled_flag has 47 relevant characters (indices 0-46).
  for ( i = 0; i <= 0x2E; ++i ) // 0x2E is 46
  {
    rotated_char = custom_rot((unsigned char)scrambled_flag[i], 37); // 37 is 0x25
    putchar(rotated_char);
    // sleep() call removed
    // fflush() is less critical here without sleep, but good for ensuring output
    fflush(stdout); 
  }
  putchar('\n'); // Print a final newline
  return 0;
} 
