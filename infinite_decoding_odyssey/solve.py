SCRAMBLED_FLAG = "V1QWz9Xq8B_q11B9Q0sBQB}s7@B143WB9Y2UB9pB57q39CA"
CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_!@#$%^&*()-+="

def rotate_char(char_to_rotate, amount, charset_str):
    try:
        idx = charset_str.find(char_to_rotate)
        if idx == -1:
            return char_to_rotate # Character not in charset, return as is
        rotated_idx = (idx - amount + len(charset_str)) % len(charset_str) # Subtracting for decryption
        return charset_str[rotated_idx]
    except Exception as e:
        # print(f"Error rotating char {char_to_rotate}: {e}")
        return char_to_rotate # Fallback

def apply_rotation_to_string(s, amount, charset_str):
    return "".join([rotate_char(c, amount, charset_str) for c in s])

if __name__ == "__main__":
    print(f"Original scrambled: {SCRAMBLED_FLAG}")
    print(f"Using charset: {CHARSET}\n")

    len_charset = len(CHARSET)
    found_meaningful = False

    # Try to find a rotation that produces the known prefix "fla"
    known_prefix = "fla"
    scrambled_prefix = SCRAMBLED_FLAG[:len(known_prefix)]

    print(f"Attempting to match prefix '{known_prefix}' from scrambled prefix '{scrambled_prefix}'...")
    for i in range(len_charset):
        # Check first char
        rotated_scrambled_char0 = rotate_char(scrambled_prefix[0], i, CHARSET)
        if rotated_scrambled_char0 == known_prefix[0]:
            # Check second char
            rotated_scrambled_char1 = rotate_char(scrambled_prefix[1], i, CHARSET)
            if rotated_scrambled_char1 == known_prefix[1]:
                # Check third char
                rotated_scrambled_char2 = rotate_char(scrambled_prefix[2], i, CHARSET)
                if rotated_scrambled_char2 == known_prefix[2]:
                    print(f"\nPotential match for '{known_prefix}' found with rotation amount: {i}")
                    decoded_string = apply_rotation_to_string(SCRAMBLED_FLAG, i, CHARSET)
                    print(f"ROTATION {i}: {decoded_string}")
                    if known_prefix in decoded_string:
                        found_meaningful = True
                        # break # Assuming first match is the one
    if not found_meaningful:
        print("Could not find rotation for 'fla' directly. Printing all rotations...")

    print("\n--- Full Rotations (looking for SKILL{ or other flag formats) ---")
    for i in range(len_charset):
        decoded_string = apply_rotation_to_string(SCRAMBLED_FLAG, i, CHARSET)
        print(f"ROTATION {i:02d}: {decoded_string}")
        if "SKILL{" in decoded_string or "flag{" in decoded_string or "CTF{" in decoded_string:
            print(f"  ^^^ Potential Flag Found at ROTATION {i}! ^^^")
            found_meaningful = True

    if not found_meaningful:
        print("\nNo common flag format found in rotations.") 
