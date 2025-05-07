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
