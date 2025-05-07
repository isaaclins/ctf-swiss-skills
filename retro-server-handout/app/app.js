const express = require('express');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);
const app = express();

app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

app.get('/', (req, res) => {
  res.render('index');
});

app.get('/healthcheck', (req, res) => {
  res.render('healthcheck', { output: null, cmd: null, arg: null });
});

app.get('/server-info', (req, res) => {
  res.render('server-info');
});

app.post('/check', async (req, res) => {
  const cmd = req.body.cmd || '';
  const arg = req.body.arg || '';
  const allowed = ['hostname', 'uptime', 'df', 'free', 'who', 'netstat'];

  const containsAllowed = allowed.some(allowedCmd => cmd.includes(allowedCmd));
  if (!containsAllowed) {
    return res.render('healthcheck', { output: 'Invalid command! Must contain one of: ' + allowed.join(', ') });
  }

  // Whitelist of allowed arguments per command
  const allowedArgs = {
    hostname: [],
    uptime: [],
    df: ['-h', '-k', '-m', '/'],
    free: ['-h', '-m', '-g'],
    who: [], 
    netstat: ['-tuln', '-a', '-p'] 
  };

  // Blacklist of blocked arguments to detect hackers
  const blacklistArgs = [';', '&&', '|', '>', '<'];

  const baseCmd = allowed.find(allowedCmd => cmd.includes(allowedCmd));

  let fullCmd = cmd;
  if (arg) {
    const argsArray = arg.trim().split(/\s+/);
    const validArgs = allowedArgs[baseCmd] || [];

    const hasBlacklisted = argsArray.some(argPart => 
      blacklistArgs.some(bad => argPart.toLowerCase().includes(bad))
    );
    if (hasBlacklisted) {
      const hackMessage = `Hacking attempt detected from IP ${req.ip} with cmd: "${cmd}" and arg: "${arg}"`;
      return res.render('healthcheck', { output: hackMessage });
    }

    const allArgsValid = argsArray.every(argPart => validArgs.includes(argPart));
    if (!allArgsValid) {
      return res.render('healthcheck', { output: `Invalid arguments for ${baseCmd}! Allowed: ${validArgs.length ? validArgs.join(', ') : 'none'}` });
    }

    fullCmd = `${cmd} ${arg}`;
  }

  try {
    const { stdout, stderr } = await execPromise(fullCmd);
    if (stderr) {
      return res.render('healthcheck', { output: stderr});
    }
    res.render('healthcheck', { output: stdout});
  } catch (error) {
    res.render('healthcheck', { output: error.message});
  }
});

app.get('/management', async (req, res) => {
  let npmPackages = [];
  let apkPackages = [];

  try {
    const { stdout: npmList } = await execPromise('npm list --depth=0 --json', { cwd: '/app' });
    const parsed = JSON.parse(npmList);
    npmPackages = Object.entries(parsed.dependencies || {}).map(([name, info]) => ({
      name,
      version: info.version
    }));
  } catch (error) {
    npmPackages.push({ name: 'Error', version: error.message });
  }

  try {
    const { stdout: apkList } = await execPromise('apk info -v');
    apkPackages = apkList.trim().split('\n').map(line => {
      const [name, version] = line.split('-').reduce((acc, part, i, arr) => {
        if (i === arr.length - 1) {
          acc[1] = part;
        } else {
          acc[0] = acc[0] ? `${acc[0]}-${part}` : part;
        }
        return acc;
      }, ['', '']);
      return { name, version };
    });
  } catch (error) {
    apkPackages.push({ name: 'Error', version: error.message });
  }

  res.render('management', { npmPackages, apkPackages });
});

app.listen(5003, '0.0.0.0', () => {
  console.log('Server running on http://0.0.0.0:5003');
});