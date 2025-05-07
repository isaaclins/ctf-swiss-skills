import sys

def caesar_decrypt(ciphertext, shift):
    decrypted_text = []
    for char in ciphertext:
        if 'a' <= char <= 'z':
            shifted_char = chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))
        elif 'A' <= char <= 'Z':
            shifted_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
        else:
            shifted_char = char
        decrypted_text.append(shifted_char)
    return "".join(decrypted_text)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python caesar_cracker.py <ciphertext>")
        sys.exit(1)

    ciphertext = sys.argv[1]

    print(f"Ciphertext: {ciphertext}\n")
    print("Attempting all Caesar cipher shifts (1-25):")
    print("---------------------------------------------")
    # Shift 0 (original text) is ciphertext itself.
    # We are interested in shifts 1 through 25 for decryption.
    # A decryption shift of S is equivalent to an encryption shift of (26-S).
    # For example, a decryption shift of 3 (to undo an encryption shift of +3)
    # is what we are looking for. This corresponds to `shift = 3` in our decrypt function.
    # A decryption shift of -3 (or +23) means `shift = 23` in our function.

    for shift_val in range(1, 26):
        # Our caesar_decrypt function interprets `shift` as the value
        # subtracted from the character.
        # So a 'shift_val' of 3 means we are trying to reverse an encryption key of +3.
        # This is equivalent to Caesar N+3, or decrypting by -3.
        # If the encryption was +3 (e.g. A -> D), we want to shift by -3 (D -> A).
        # In our function, `shift = 3` will do `ord(char) - ord('A') - 3`.
        
        # Let's clarify the output to represent the "key" or effective "negative shift"
        # If ciphertext C was P + K (mod 26), then P = C - K (mod 26).
        # Our shift_val is K.
        
        decrypted = caesar_decrypt(ciphertext, shift_val)
        # We want to show the shift that was *undone*.
        # If our function used `shift_val = 3`, it means it undid an encryption of +3.
        print(f"Undoing shift +{shift_val:02d} (or trying key -{shift_val:02d}): {decrypted}")

    print("\nReminder: Our target shift was -3 (or +23).")
    print("In the output above, 'Undoing shift +03' is equivalent to decrypting with -3.")
    print("And 'Undoing shift +23' is equivalent to decrypting with -23 (or +3).")
    print("So you are looking for the output of 'Undoing shift +03' for our current hypothesis.") 
