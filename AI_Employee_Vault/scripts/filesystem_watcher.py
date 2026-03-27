"""
File System Watcher for AI Employee (Bronze Tier)

Monitors a drop folder for new files and creates action files in Needs_Action.
This is the simpler alternative to Gmail watcher for Bronze tier.

Usage:
    python filesystem_watcher.py /path/to/vault

Or edit VAULT_PATH below to point to your Obsidian vault.
"""

import sys
import time
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from base_watcher import BaseWatcher, logging

# Configure this path to point to your Obsidian vault
VAULT_PATH = Path(__file__).parent.parent  # Points to AI_Employee_Vault
DROP_FOLDER = VAULT_PATH / 'Inbox'


class DropFolderHandler(FileSystemEventHandler):
    """
    Handles file creation events in the drop folder.
    Copies new files to Needs_Action and creates metadata files.
    """
    
    def __init__(self, vault_path: str):
        """
        Initialize the handler.
        
        Args:
            vault_path: Path to the Obsidian vault root
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Ensure folders exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        
        # Track processed files by hash to avoid duplicates
        self.processed_hashes = set()
    
    def on_created(self, event):
        """
        Handle file creation events.
        
        Args:
            event: File system event
        """
        if event.is_directory:
            return
        
        source = Path(event.src_path)
        
        # Skip hidden files and temporary files
        if source.name.startswith('.') or source.suffix == '.tmp':
            return
        
        # Skip if already processed
        file_hash = self._hash_file(source)
        if file_hash in self.processed_hashes:
            return
        
        self.logger.info(f'New file detected: {source.name}')
        
        # Copy file to Needs_Action
        dest = self.needs_action / f'FILE_{source.name}'
        try:
            shutil.copy2(source, dest)
            self.logger.info(f'Copied to: {dest}')
        except Exception as e:
            self.logger.error(f'Error copying file: {e}')
            return
        
        # Create metadata file
        meta_path = self.create_metadata(source, dest)
        self.logger.info(f'Created metadata: {meta_path.name}')
        
        # Mark as processed
        self.processed_hashes.add(file_hash)
    
    def _hash_file(self, filepath: Path) -> str:
        """
        Create a hash of the file for deduplication.
        
        Args:
            filepath: Path to the file
            
        Returns:
            MD5 hash of file contents
        """
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return str(filepath)
    
    def create_metadata(self, source: Path, dest: Path) -> Path:
        """
        Create a Markdown metadata file for the dropped file.
        
        Args:
            source: Original file path
            dest: Destination file path in Needs_Action
            
        Returns:
            Path to the created metadata file
        """
        meta_path = dest.with_suffix('.md')
        
        content = f'''---
type: file_drop
original_name: {source.name}
size: {source.stat().st_size}
created: {datetime.now().isoformat()}
status: pending
---

# File Drop for Processing

**Original File:** `{source.name}`

**Size:** {self._format_size(source.stat().st_size)}

**Dropped At:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Location:** `{dest}`

---

## Suggested Actions

- [ ] Review file contents
- [ ] Process or take action
- [ ] Move to /Done when complete

## Notes

*Add notes about processing this file below*

'''
        meta_path.write_text(content)
        return meta_path
    
    def _format_size(self, size_bytes: int) -> str:
        """
        Format file size in human-readable format.
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted string (e.g., "1.5 MB")
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"


class FilesystemWatcher(BaseWatcher):
    """
    Watcher that uses watchdog to monitor a folder for new files.
    """
    
    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the filesystem watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Not used (watchdog is event-driven)
        """
        super().__init__(vault_path, check_interval)
        self.drop_folder = self.vault_path / 'Inbox'
        self.drop_folder.mkdir(parents=True, exist_ok=True)
    
    def check_for_updates(self) -> list:
        """
        Not used - watchdog is event-driven.
        This method is required by the abstract base class.
        
        Returns:
            Empty list
        """
        return []
    
    def create_action_file(self, item) -> Path:
        """
        Not used - handled by DropFolderHandler.
        This method is required by the abstract base class.
        
        Args:
            item: Ignored
            
        Returns:
            None
        """
        pass
    
    def run(self):
        """
        Run the watchdog observer.
        """
        self.logger.info(f'Starting FilesystemWatcher')
        self.logger.info(f'Monitoring: {self.drop_folder}')
        
        event_handler = DropFolderHandler(str(self.vault_path))
        observer = Observer()
        observer.schedule(event_handler, str(self.drop_folder), recursive=False)
        observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            self.logger.info('Watcher stopped')
        observer.join()


if __name__ == '__main__':
    # Allow vault path override via command line
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = str(VAULT_PATH)
    
    watcher = FilesystemWatcher(vault_path)
    watcher.run()
