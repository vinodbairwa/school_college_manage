#!/usr/bin/env node
/**
 * Cross-platform EduNest starter (Windows / macOS / Linux)
 * Starts: FastAPI backend :8000 + Next.js website :3000 + React panel :5173
 */
import { spawn, spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const isWin = process.platform === "win32";

function exists(p) {
  return fs.existsSync(p);
}

function run(cmd, args, opts = {}) {
  const result = spawnSync(cmd, args, {
    cwd: opts.cwd || ROOT,
    stdio: "inherit",
    shell: opts.shell ?? false,
    env: { ...process.env, ...(opts.env || {}) },
  });
  if (result.status !== 0) {
    throw new Error(`Command failed (${result.status}): ${cmd} ${args.join(" ")}`);
  }
}

function resolvePython() {
  const candidates = isWin
    ? [
        path.join(ROOT, ".venv", "Scripts", "python.exe"),
        "py",
        "python",
        "python3",
      ]
    : [
        path.join(ROOT, ".venv", "bin", "python"),
        "python3",
        "python",
      ];

  for (const c of candidates) {
    if (c.includes("path.sep") || c.includes("/") || c.includes("\\")) {
      if (exists(c)) return { cmd: c, argsPrefix: [] };
      continue;
    }
    const probe = spawnSync(c, ["--version"], { encoding: "utf8" });
    if (probe.status === 0) {
      if (c === "py") return { cmd: "py", argsPrefix: ["-3"] };
      return { cmd: c, argsPrefix: [] };
    }
  }
  throw new Error("Python 3 not found. Install Python 3.12+ and retry.");
}

function venvPython() {
  const p = isWin
    ? path.join(ROOT, ".venv", "Scripts", "python.exe")
    : path.join(ROOT, ".venv", "bin", "python");
  if (!exists(p)) {
    throw new Error(`Virtualenv python missing at ${p}. Run setup again.`);
  }
  return p;
}

function ensureFile(src, dest) {
  if (!exists(dest) && exists(src)) {
    fs.copyFileSync(src, dest);
    console.log(`Created ${path.relative(ROOT, dest)}`);
  }
}

function setup() {
  console.log("==> EduNest setup");
  console.log("    backend : http://127.0.0.1:8000");
  console.log("    website : http://127.0.0.1:3000");
  console.log("    panel   : http://127.0.0.1:5173\n");

  const py = resolvePython();
  const venvDir = path.join(ROOT, ".venv");
  if (!exists(venvDir)) {
    console.log("==> Creating Python virtualenv (.venv)...");
    run(py.cmd, [...py.argsPrefix, "-m", "venv", ".venv"]);
  }

  const vpy = venvPython();
  console.log("==> Installing backend Python packages...");
  run(vpy, ["-m", "pip", "install", "-r", "backend/requirements.txt"]);

  ensureFile(path.join(ROOT, "backend", ".env.example"), path.join(ROOT, "backend", ".env"));
  ensureFile(
    path.join(ROOT, "website", ".env.local.example"),
    path.join(ROOT, "website", ".env.local")
  );
  ensureFile(path.join(ROOT, "panel", ".env.example"), path.join(ROOT, "panel", ".env"));

  console.log("==> Seeding database...");
  run(vpy, ["seed.py"], { cwd: path.join(ROOT, "backend") });

  if (!exists(path.join(ROOT, "node_modules"))) {
    console.log("==> Installing root npm packages...");
    run(isWin ? "npm.cmd" : "npm", ["install"], { shell: isWin });
  }
  if (!exists(path.join(ROOT, "website", "node_modules"))) {
    console.log("==> Installing website packages...");
    run(isWin ? "npm.cmd" : "npm", ["--prefix", "website", "install"], { shell: isWin });
  }
  if (!exists(path.join(ROOT, "panel", "node_modules"))) {
    console.log("==> Installing panel packages...");
    run(isWin ? "npm.cmd" : "npm", ["--prefix", "panel", "install"], { shell: isWin });
  }
}

function spawnProc(name, cmd, args, cwd) {
  const child = spawn(cmd, args, {
    cwd,
    stdio: "inherit",
    shell: isWin,
    env: process.env,
  });
  child.on("exit", (code, signal) => {
    console.log(`[${name}] exited code=${code} signal=${signal || ""}`);
    shutdown(code || 1);
  });
  return child;
}

const children = [];
let shuttingDown = false;

function shutdown(code = 0) {
  if (shuttingDown) return;
  shuttingDown = true;
  for (const child of children) {
    try {
      if (!child.killed) child.kill("SIGTERM");
    } catch {
      // ignore
    }
  }
  process.exit(code);
}

process.on("SIGINT", () => shutdown(0));
process.on("SIGTERM", () => shutdown(0));

const skipSetup = process.argv.includes("--skip-setup");
const seedOnly = process.argv.includes("--seed-only");

try {
  if (!skipSetup || seedOnly || !exists(path.join(ROOT, ".venv"))) {
    setup();
  } else if (!seedOnly) {
    // still seed quickly (idempotent)
    const vpy = venvPython();
    run(vpy, ["seed.py"], { cwd: path.join(ROOT, "backend") });
  }

  if (seedOnly) {
    process.exit(0);
  }

  const vpy = venvPython();
  const npm = isWin ? "npm.cmd" : "npm";

  console.log("\n==> Starting backend + website + panel...\n");

  children.push(
    spawnProc(
      "backend",
      vpy,
      ["-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
      path.join(ROOT, "backend")
    )
  );
  children.push(
    spawnProc("website", npm, ["run", "dev", "--", "-H", "0.0.0.0", "-p", "3000"], path.join(ROOT, "website"))
  );
  children.push(
    spawnProc("panel", npm, ["run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"], path.join(ROOT, "panel"))
  );
} catch (err) {
  console.error("\nERROR:", err.message || err);
  console.error("\nManual backend check:");
  console.error("  cd backend");
  console.error(isWin ? "  ..\\.venv\\Scripts\\python -m uvicorn app.main:app --reload --port 8000" : "  source ../.venv/bin/activate && uvicorn app.main:app --reload --port 8000");
  process.exit(1);
}
