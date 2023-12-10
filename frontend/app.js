const { spawn } = require('child_process');

// Run subscribe.py
const subscribeProcess = spawn('python3', ['subscribe.py']);

// Log stdout and stderr from subscribe.py
subscribeProcess.stdout.on('data', (data) => {
  console.log(`subscribe.py stdout: ${data}`);
});

subscribeProcess.stderr.on('data', (data) => {
  console.error(`subscribe.py stderr: ${data}`);
});

subscribeProcess.on('close', (code) => {
  console.log(`subscribe.py process exited with code ${code}`);
});
