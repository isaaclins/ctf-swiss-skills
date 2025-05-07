## Command Injection Vulnerability in Retro Server

The vulnerability lies in the `/healthcheck` endpoint, specifically how it processes the `cmd` and `arg` parameters.

### Vulnerability Analysis

The provided code snippet from `app/app.js` shows the following logic:

```javascript
// Blacklist of blocked arguments to detect hackers
const blacklistArgs = [";", "&&", "|", ">", "<"];

const baseCmd = allowed.find((allowedCmd) => cmd.includes(allowedCmd));

let fullCmd = cmd;
if (arg) {
  const argsArray = arg.trim().split(/\s+/);
  const validArgs = allowedArgs[baseCmd] || [];

  const hasBlacklisted = argsArray.some((argPart) =>
    blacklistArgs.some((bad) => argPart.toLowerCase().includes(bad))
  );
  if (hasBlacklisted) {
    const hackMessage = `Hacking attempt detected from IP ${req.ip} with cmd: "${cmd}" and arg: "${arg}"`;
    return res.render("healthcheck", { output: hackMessage });
  }

  const allArgsValid = argsArray.every((argPart) =>
    validArgs.includes(argPart)
  );
  if (!allArgsValid) {
    return res.render("healthcheck", {
      output: `Invalid arguments for ${baseCmd}! Allowed: ${
        validArgs.length ? validArgs.join(", ") : "none"
      }`,
    });
  }

  fullCmd = `${cmd} ${arg}`;
}

try {
  const { stdout, stderr } = await execPromise(fullCmd);
  if (stderr) {
    return res.render("healthcheck", { output: stderr });
  }
  res.render("healthcheck", { output: stdout });
} catch (error) {
  res.render("healthcheck", { output: error.message });
}
```

1.  The code checks for blacklisted characters (`;`, `&&`, `|`, `>`, `<`) and validates arguments _only if the `arg` parameter is provided_.
2.  If the `arg` parameter is missing or empty, the validation block is skipped.
3.  In this case, `fullCmd` is set directly to the value of the `cmd` parameter.
4.  This `fullCmd` is then executed on the server using `execPromise(fullCmd)`.

This means we can inject arbitrary commands by sending a `cmd` parameter containing a command separator (like `;`) followed by our desired command, and omitting the `arg` parameter (or sending it as an empty string).

### Exploitation Steps

1.  **Identify an Allowed Command**:
    The application has a list of `allowed` commands. The `baseCmd` is derived from the `cmd` parameter if it contains one of these allowed commands. We need to find or guess one of these. Common commands like `ping`, `ls`, `echo`, `date` are good candidates to try. Let's assume `ping` is an allowed command for this example.

2.  **Craft the Payload**:
    To execute `cat /etc/passwd` (as an example for reading a file), the payload would be:

    - `cmd` parameter: `ping; cat /etc/passwd`
    - `arg` parameter: (omit this parameter or send it as an empty string)

3.  **Send the Request**:
    The request would likely be a GET or POST request to the `/healthcheck` endpoint. Based on the `README.md`, the base URL is `https://cyberskills.ch:5003/`.
    So, an example request URL could be:
    `https://cyberskills.ch:5003/healthcheck?cmd=ping%3B%20cat%20%2Fetc%2Fpasswd`

    (Note: `%3B` is the URL encoding for `;` and `%20` is for space. Ensure your HTTP client or browser correctly encodes these if you type them directly.)

### Example Solution (to read a flag file)

Assuming the flag is in a file named `flag.txt` in the current directory or a known path:

1.  **Find an allowed command**: Try sending `ping` as the `cmd` parameter with no `arg` parameter. If it works, `ping` is allowed.
    `https://cyberskills.ch:5003/healthcheck?cmd=ping`

2.  **Construct the payload to read `flag.txt`**:
    `cmd=ping; cat flag.txt`

3.  **Send the malicious request**:
    `https://cyberskills.ch:5003/healthcheck?cmd=ping%3B%20cat%20flag.txt`

If `ping` is not allowed, try other common commands until one is found to be part of the `allowed` list. The key is that the argument validation and blacklist check are bypassed if the `arg` parameter is not present in the request.
