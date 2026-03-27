#!/usr/bin/env python3
"""
Bronze Tier Verification Script

Verifies that all Bronze tier requirements are met:
- Obsidian vault with Dashboard.md and Company_Handbook.md
- One working Watcher script (File System monitoring)
- Basic folder structure: /Inbox, /Needs_Action, /Done
"""

import sys
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def check(condition, message):
    """Print check result with color."""
    if condition:
        print(f"{GREEN}✓{RESET} {message}")
        return True
    else:
        print(f"{RED}✗{RESET} {message}")
        return False

def verify_bronze_tier(vault_path: Path) -> bool:
    """
    Verify all Bronze tier requirements.
    
    Args:
        vault_path: Path to the Obsidian vault
        
    Returns:
        True if all checks pass
    """
    print(f"\n{YELLOW}=== Bronze Tier Verification ==={RESET}\n")
    print(f"Vault: {vault_path}\n")
    
    checks = []
    
    # Required files
    print(f"{YELLOW}Checking Required Files...{RESET}")
    checks.append(check(
        (vault_path / 'Dashboard.md').exists(),
        'Dashboard.md exists'
    ))
    checks.append(check(
        (vault_path / 'Company_Handbook.md').exists(),
        'Company_Handbook.md exists'
    ))
    checks.append(check(
        (vault_path / 'Business_Goals.md').exists(),
        'Business_Goals.md exists'
    ))
    checks.append(check(
        (vault_path / 'README.md').exists(),
        'README.md exists'
    ))
    
    # Required folders
    print(f"\n{YELLOW}Checking Required Folders...{RESET}")
    required_folders = ['Inbox', 'Needs_Action', 'Done', 'Pending_Approval', 'Approved', 'Rejected']
    for folder in required_folders:
        checks.append(check(
            (vault_path / folder).exists(),
            f'/{folder} folder exists'
        ))
    
    # Watcher scripts
    print(f"\n{YELLOW}Checking Watcher Scripts...{RESET}")
    scripts_path = vault_path / 'scripts'
    checks.append(check(
        scripts_path.exists(),
        'scripts/ folder exists'
    ))
    checks.append(check(
        (scripts_path / 'base_watcher.py').exists(),
        'base_watcher.py exists (template)'
    ))
    checks.append(check(
        (scripts_path / 'filesystem_watcher.py').exists(),
        'filesystem_watcher.py exists (Bronze tier watcher)'
    ))
    
    # Verify watcher can be imported
    print(f"\n{YELLOW}Checking Watcher Functionality...{RESET}")
    try:
        sys.path.insert(0, str(scripts_path))
        from filesystem_watcher import FilesystemWatcher
        checks.append(check(True, 'filesystem_watcher.py imports successfully'))
    except Exception as e:
        checks.append(check(False, f'filesystem_watcher.py import failed: {e}'))
    
    try:
        from base_watcher import BaseWatcher
        checks.append(check(True, 'base_watcher.py imports successfully'))
    except Exception as e:
        checks.append(check(False, f'base_watcher.py import failed: {e}'))
    
    # Test file
    print(f"\n{YELLOW}Checking Test Files...{RESET}")
    needs_action = vault_path / 'Needs_Action'
    test_files = list(needs_action.glob('TEST_*.md'))
    checks.append(check(
        len(test_files) > 0,
        'Test file exists in /Needs_Action (TEST_*.md)'
    ))
    
    # Summary
    print(f"\n{YELLOW}=== Summary ==={RESET}")
    passed = sum(checks)
    total = len(checks)
    percentage = (passed / total) * 100 if total > 0 else 0
    
    if percentage == 100:
        print(f"\n{GREEN}✓ All {total} checks passed! Bronze tier complete.{RESET}\n")
        return True
    else:
        print(f"\n{RED}✗ {total - passed} of {total} checks failed.{RESET}")
        print(f"  Passed: {passed}/{total} ({percentage:.0f}%)\n")
        return False


if __name__ == '__main__':
    # Default vault path
    vault_path = Path(__file__).parent.parent
    
    # Allow override via command line
    if len(sys.argv) > 1:
        vault_path = Path(sys.argv[1])
    
    success = verify_bronze_tier(vault_path)
    sys.exit(0 if success else 1)
