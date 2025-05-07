# I Like Dolphins CTF Solution

The challenge involves a PowerShell script (`I_like_dolphins.ps1`) that contains multiple layers of Base64 encoded PowerShell commands.

## Steps to Solve

1.  **Initial File Content**:
    The file `I_like_dolphins.ps1` contains a single line:

    ```powershell
    iex([System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String('aWV4KFtTeXN0ZW0uVGV4dC5FbmNvZGluZ106OkFTQ0lJLkdldFN0cmluZyhbU3lzdGVtLkNvbnZlcnRdOjpGcm9tQmFzZTY0U3RyaW5nKCdKRUU5SnoxclUwdHdhM2xLYmtGcFluQTViV0YwUVZOWWR6UnBURzlTTTFwMVZrZFVkVVZGU21KR1JVcHZaM2xhZFd4dFl6Qk9SazR5VlRKamFFcFZZblpLYmxJMmIxUllNRXBZV2pJMU1tSkVkRVpMYmpWWFlYbFNNMVV3VmpKU2RXdFZVMFJPVmxFMmIxUllialZYWVdzNU1sbDFWbXRNTUdoWVdsVjBSa3RuWjFoYWNFSjVUMjVyVldWRE1XMVpTRnByWW14Q2Vsb3pVbGROTlhOWFZGaEtiRnBzWkZaUGVHZHNUVnBvYmxsMFNteGFhV2hHWW0xd1JsSkRUak5aU0hoWFpGRk9SRTFNV2pGTlMwSklXa2hXUm1SVVpGVlBObEl5VVVKc01sVlVTakJqYUdSR1pITnNNRkpUV201WlNVb3dZbWhrVms0MmJEQlZRMDVGV2xsR01WcFVUbXhSZWtsdFRURkJWRk5JUWxoTmFrNVVWVzVPUjFOTFFtNVpkVVl4V214a1ZrOTRhMFZUVXpsdFYxUktWV0pwWkd0U2RYaFZZVW94ZWtvNVJVVktKenNnYVdWNElDaGJWR1Y0ZEM1RmJtTnZaR2x1WjEwNk9rRlRRMGxKTGtkbGRGTjBjbWx1WnloYlEyOXVkbVZ5ZEYwNk9rWnliMjFDWVhObE5qUlRkSEpwYm1jb0tDUkJXeVJCTGt4bGJtZDBhQzR1TUYwZ0xXcHZhVzRnSnljcEtTa3AnKSkp')))
    ```

    This command decodes the outer Base64 string and executes the result using `iex` (Invoke-Expression).

2.  **First Layer Decoded**:
    Decoding the first Base64 string (`aWV4K...Ta3AnKSkp`) yields another PowerShell command:

    ```powershell
    iex([System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String('KRU9Jz1rU0twa3xLYbGcFlnA5bWF0QVNYdzRpTG9SM1p1VVkdVVFGUmJGRUpvZ3JhZFxtdFl6Qk9SazR5VlRKamFFcFZZblpLYmxJMmIxUllNRXBZV2pJMU1tSkVkRVpMYmpWWFlYbFNNMVV3VmpKU2RXdFZVMFJPVmxFMmIxUllialZYWVdzNU1sbDFWbXRNTUdoWVdsVjBSa3RuWjFoYWNFSjVUMjVyVldWRE1XMVpTRnByWW14Q2Vsb3pVbGROTlhOWFZGaEtiRnBzWkZaUGVHZHNUVnBvYmxsMFNteGFhV2hHWW0xd1JsSkRUak5aU0hoWFpGRk9SRTFNV2pGTlMwSklXa2hXUm1SVVpGVlBObEl5VVVKc01sVlVTakJqYUdSR1pITnNNRkpUV201WlNVb3dZbWhrVms0MmJEQlZRMDVGV2xsR01WcFVUbXhSZWtsdFRURkJWRk5JUWxoTmFrNVVWVzVPUjFOTFFtNVpkVVl4V214a1ZrOTRhMFZUVXpsdFYxUktWV0pwWkd0U2RYaFZZVW94ZWtvNVJVVktKenNnYVdWNElDaGJWR1Y0ZEM1RmJtTnZaR2x1WjEwNk9rRlRRMGxKTGtkbGRGTjBjbWx1WnloYlEyOXVkbVZ5ZEYwNk9rWnliMjFDWVhObE5qUlRkSEpwYm1jb0tDUkJXeVJCTGt4bGJtZDBhQzR1TUYwZ0xXcHZhVzRnSnljcEtTa3A=')))
    ```

    This is also an `iex` command that decodes an inner Base64 string and executes it.

3.  **Second Layer Decoded (The Script with the Flag)**:
    Decoding the second Base64 string (`KRU9J...Ta3A=`) reveals the following PowerShell script:

    ```powershell
    $A='=kSKpk|KbgXFga9maAtASXw4iLoR3ZuUYhUQFbRFEJograd\mtTzBOSk4yVTJZhmFFpYYnZLbXJmIxUSYNpJWjM1SkRVpMYmpXFYbFNNMVVwVmpKSlV0ZVMFRNVlExbRYbjVYWs5Ml1VmMMGZYWlVBSnZjFoacEJ5T25rVVdWMW1ZSnByYmxCelUldNXNXVhFbiFPzZPUGdVnvbmxsMFMxaaWhGWmd1JlJDTjZShXZGRk9SExNVpGTlMjJVakRXUmVUaFVBblI5VUlKc0xlVVJqYUdaZFlITklNVTNLWkVSWVdZbWs0MmJDUVFVRlVsR01WUFVUbVhSZWtsdFRURkJVRk5JUWxoTmFrNVVWVzVPUjFOTFFtNVpkVVl4V214a1ZrOTRhMFZUVXpsdFYxUktWV0pwWkd0U2RYaFZZVW94ZWtvNVJVVktKenNnYVY0IChbSystem.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String('SSdtIGluc2lkZSBhIGRvbHBoaW4ncyBtaW5kLCB0aGUgZmxhZyBpcyBTU0NUIHtEMGxwSElOU19HMDBEX0QwdGhpTkd9')))
    ```

    This script assigns a string to variable `$A`. The crucial part is `[System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String('SSdtIGluc2lkZSBhIGRvbHBoaW4ncyBtaW5kLCB0aGUgZmxhZyBpcyBTU0NUIHtEMGxwSElOU19HMDBEX0QwdGhpTkd9'))`, which decodes the final Base64 string containing the flag.

4.  **Final Base64 String for the Flag**:
    The Base64 string containing the flag is:
    `SSdtIGluc2lkZSBhIGRvbHBoaW4ncyBtaW5kLCB0aGUgZmxhZyBpcyBTU0NUIHtEMGxwSElOU19HMDBEX0QwdGhpTkd9`

5.  **Decoding the Flag**:
    Decoding this string from Base64 (ASCII encoded) gives:

    ```
    I'm inside a dolphin's mind, the flag is SSCT {D0lpHINS_G00D_D0thiNG}
    ```

6.  **Python Script for Automation**:
    The following Python script (`decode_script.py`) can be used to directly decode the final Base64 string:

    ```python
    import base64

    # The original file I_like_dolphins.ps1 contains:
    # iex([System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String('aWV4K...NTa3AnKSkp')))
    #
    # Decoding 'aWV4K...NTa3AnKSkp' gives:
    # iex([System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String('KRU9J...Ta3A=')))
    #
    # Decoding 'KRU9J...Ta3A=' gives the following PowerShell script:
    # $A='=kSKpk|KbgXFga9maAtASXw4iLoR3ZuUYhUQFbRFEJograd\mtTzBOSk4yVTJZhmFFpYYnZLbXJmIxUSYNpJWjM1SkRVpMYmpXFYbFNNMVVwVmpKSlV0ZVMFRNVlExbRYbjVYWs5Ml1VmMMGZYWlVBSnZjFoacEJ5T25rVVdWMW1ZSnByYmxCelUldNXNXVhFbiFPzZPUGdVnvbmxsMFMxaaWhGWmd1JlJDTjZShXZGRk9SExNVpGTlMjJVakRXUmVUaFVBblI5VUlKc0xlVVJqYUdaZFlITklNVTNLWkVSWVdZbWs0MmJDUVFVRlVsR01WUFVUbVhSZWtsdFRURkJVRk5JUWxoTmFrNVVWVzVPUjFOTFFtNVpkVVl4V214a1ZrOTRhMFZUVXpsdFYxUktWV0pwWkd0U2RYaFZZVW94ZWtvNVJVVktKenNnYVY0IChbSystem.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String('SSdtIGluc2lkZSBhIGRvbHBoaW4ncyBtaW5kLCB0aGUgZmxhZyBpcyBTU0NUIHtEMGxwSElOU19HMDBEX0QwdGhpTkd9')))
    #
    # The crucial part is the final Base64 encoded string within that script:
    final_encoded_part = "SSdtIGluc2lkZSBhIGRvbHBoaW4ncyBtaW5kLCB0aGUgZmxhZyBpcyBTU0NUIHtEMGxwSElOU19HMDBEX0QwdGhpTkd9"

    flag = base64.b64decode(final_encoded_part).decode('ascii')
    print("--- Final Decoded Flag ---")
    print(flag)
    ```

    Running this script (`python3 i_like_dolphins/decode_script.py`) will print the decoded flag.

## The Flag

`SSCT {D0lpHINS_G00D_D0thiNG}`
