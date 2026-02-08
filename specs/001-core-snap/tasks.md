# Tasks: Core Snap Implementation

## Phase 1: Environment & Foundation [P]
- [ ] Initialize Python project with `uv init --lib`
- [ ] Add dependencies: `click`, `mss`, `playwright`, `pillow`, `pygetwindow`
- [ ] Create directory structure: `src/paparazzit/capture`, `src/paparazzit/utils`
- [ ] Create `captures/` output directory with `.gitignore`

## Phase 2: Utilities [P]
- [ ] Implement `storage.py`: Handle file naming (timestamp-based) and PNG/JSON saving
- [ ] Implement `metadata.py`: Gather system info (OS, resolution, timestamp)

## Phase 3: Capture Engines
- [ ] Implement `engine.py`: Define the `BaseCaptureEngine` interface
- [ ] Implement `playwright_engine.py`: Handle URL captures with automatic browser check/install
- [ ] Implement `mss_engine.py`: Handle window-based captures and cropping logic

## Phase 4: CLI & Integration
- [ ] Implement `cli.py`: Define `snap` command with `--url` and `--window` flags
- [ ] Add `paparazzit` entry point to `pyproject.toml`
- [ ] Final integration testing: Snap a URL and snap a window

## Phase 5: Documentation & Cleanup
- [ ] Update `README.md` with usage instructions
- [ ] Commit all changes to git
