import os
import pytest
from paparazzit.utils.storage import PROJECT_ROOT, DEFAULT_CAPTURES_DIR

def test_project_root_detection():
    # Since we are running in the repo, PROJECT_ROOT should point to the repo root
    assert os.path.exists(os.path.join(PROJECT_ROOT, "pyproject.toml"))

def test_env_var_override(monkeypatch):
    test_path = "/tmp/paparazzit_test_root"
    monkeypatch.setenv("PAPARAZZIT_ROOT", test_path)
    
    # We need to reload or re-evaluate the storage logic. 
    # Since PROJECT_ROOT is a module-level constant, we'll check how it behaves 
    # if we were to re-import or just check the logic directly if possible.
    # For a clean test of the logic without side effects on other tests:
    
    import importlib
    import paparazzit.utils.storage
    importlib.reload(paparazzit.utils.storage)
    
    assert paparazzit.utils.storage.PROJECT_ROOT == test_path
    assert paparazzit.utils.storage.DEFAULT_CAPTURES_DIR == os.path.join(test_path, "captures", "snaps")
    
    # Cleanup for other tests
    monkeypatch.delenv("PAPARAZZIT_ROOT", raising=False)
    importlib.reload(paparazzit.utils.storage)
