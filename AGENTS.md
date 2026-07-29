# AGENTS.md

Guidance for AI agents working in this repository.

## Project status

`school_college_manage` is currently a **scaffold repository**. It contains only `README.md` with the project title. There is no application source code, dependency manifests, build configuration, tests, or lint setup yet.

## Cursor Cloud specific instructions

### Available runtimes

The Cloud Agent VM includes common development tooling:

| Tool | Notes |
|------|-------|
| Node.js | v22.x via nvm (`/home/ubuntu/.nvm/versions/node/v22.22.2/bin/`) |
| npm / pnpm / yarn | Available alongside Node |
| Python | 3.12 (`python3`, `pip`) |
| Go | `/usr/bin/go` |
| Rust | `/usr/local/cargo/bin/rustc` |
| Java | `/usr/bin/java` |

### Services

There are **no services to start** until application code is added. No database, API server, or frontend dev server is defined in this repo.

### Lint / test / build

No lint, test, or build commands exist yet. Once a stack is chosen (e.g. `package.json`, `pyproject.toml`), add the standard commands here and to the VM update script.

### Git

- Default branch: `main`
- Remote: `origin` → `github.com/vinodbairwa/school_college_manage`

### When application code is added

Update this file with:

1. Dependency install command (for the VM update script)
2. How to start required services (database, API, frontend)
3. Lint and test commands
4. Any non-obvious environment variables or secrets
