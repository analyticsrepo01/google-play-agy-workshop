import { spawnSync } from 'node:child_process';

const [major = 0, minor = 0] = process.versions.node.split('.').map(Number);
if (major < 24 || (major === 24 && minor < 13)) {
  throw new Error('ADK workshop requires Node.js 24.13.0 or newer.');
}
const npm = spawnSync(
  process.platform === 'win32' ? 'npm.cmd' : 'npm',
  ['--version'],
  { encoding: 'utf8', shell: process.platform === 'win32' },
);
if (npm.error) {
  throw npm.error;
}
if (npm.status !== 0) {
  throw new Error(`Cannot check npm: ${npm.stderr}`);
}
const [npmMajor = 0, npmMinor = 0] = npm.stdout.trim().split('.').map(Number);
if (npmMajor < 11 || (npmMajor === 11 && npmMinor < 8)) {
  throw new Error('ADK workshop requires npm 11.8.0 or newer.');
}
console.log(`Node ${process.version}; npm ${npm.stdout.trim()}`);
console.log(`Live model: ${process.env.GEMINI_MODEL ?? 'gemini-flash-latest'}`);
if (!process.env.GEMINI_API_KEY?.trim()) {
  console.error('LIVE MODE NOT READY: GEMINI_API_KEY is absent. Offline tools/tests still work; no automatic fallback.');
  process.exitCode = 1;
} else {
  console.log('GEMINI_API_KEY is set (value not displayed). Model access, quota, and connectivity still need a live smoke test.');
}
