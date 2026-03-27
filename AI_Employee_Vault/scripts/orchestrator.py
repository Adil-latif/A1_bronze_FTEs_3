"""
Orchestrator for AI Employee (Bronze Tier)

Master process that:
1. Starts and monitors watcher processes
2. Triggers Claude Code to process tasks
3. Updates Dashboard.md with status

Usage:
    python orchestrator.py [--vault PATH] [--interval SECONDS]
"""

import sys
import time
import subprocess
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class Orchestrator:
    """
    Main orchestrator for the AI Employee system.
    
    Manages watcher processes and triggers Claude Code to process tasks.
    """
    
    def __init__(self, vault_path: str, check_interval: int = 300):
        """
        Initialize the orchestrator.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Seconds between Claude processing runs (default: 300 = 5 min)
        """
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)
        self.scripts_path = self.vault_path / 'scripts'
        self.needs_action = self.vault_path / 'Needs_Action'
        self.dashboard = self.vault_path / 'Dashboard.md'
        
        # Watcher processes
        self.watcher_processes = {}
        
        # Ensure folders exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
    
    def start_watcher(self, watcher_name: str, script: str):
        """
        Start a watcher process.
        
        Args:
            watcher_name: Name for the watcher (e.g., 'filesystem')
            script: Script filename to run
        """
        script_path = self.scripts_path / script
        
        if not script_path.exists():
            self.logger.warning(f'Script not found: {script_path}')
            return
        
        self.logger.info(f'Starting {watcher_name} watcher...')
        
        try:
            # Start watcher as background process
            proc = subprocess.Popen(
                [sys.executable, str(script_path), str(self.vault_path)],
                cwd=str(self.scripts_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.watcher_processes[watcher_name] = proc
            self.logger.info(f'{watcher_name} watcher started (PID: {proc.pid})')
        except Exception as e:
            self.logger.error(f'Failed to start {watcher_name}: {e}')
    
    def stop_watchers(self):
        """Stop all watcher processes."""
        for name, proc in self.watcher_processes.items():
            self.logger.info(f'Stopping {name} watcher...')
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
            self.logger.info(f'{name} watcher stopped')
        self.watcher_processes.clear()
    
    def check_needs_action(self) -> int:
        """
        Count files in Needs_Action folder.
        
        Returns:
            Number of pending task files
        """
        if not self.needs_action.exists():
            return 0
        
        # Count .md files (excluding test files)
        md_files = list(self.needs_action.glob('*.md'))
        return len([f for f in md_files if not f.name.startswith('TEST_')])
    
    def trigger_claude(self):
        """
        Trigger Claude Code to process pending tasks.
        
        Note: This logs the action. For actual Claude execution,
        user needs to run 'claude' command interactively.
        """
        pending_count = self.check_needs_action()
        
        if pending_count == 0:
            self.logger.info('No pending tasks in /Needs_Action')
            return
        
        self.logger.info(f'Found {pending_count} pending task(s)')
        self.logger.info('To process tasks, run: claude')
        self.logger.info('Then prompt: "Process all files in /Needs_Action"')
        
        # Update dashboard with last check time
        self.update_dashboard(pending_count)
    
    def update_dashboard(self, pending_count: int):
        """
        Update Dashboard.md with current status.
        
        Args:
            pending_count: Number of pending tasks
        """
        if not self.dashboard.exists():
            self.logger.warning('Dashboard.md not found')
            return
        
        try:
            content = self.dashboard.read_text()
            
            # Update last_updated timestamp
            now = datetime.now().isoformat()
            if 'last_updated:' in content:
                # Replace existing timestamp
                import re
                content = re.sub(
                    r'last_updated:.*',
                    f'last_updated: {now}',
                    content
                )
            else:
                # Add after first ---
                content = content.replace(
                    '---\n',
                    f'---\nlast_updated: {now}\n',
                    1
                )
            
            # Update pending tasks count
            if 'Pending Tasks |' in content:
                content = re.sub(
                    r'\| Pending Tasks \|.*\|',
                    f'| Pending Tasks | {pending_count} |',
                    content
                )
            
            self.dashboard.write_text(content)
            self.logger.info('Dashboard updated')
        except Exception as e:
            self.logger.error(f'Error updating dashboard: {e}')
    
    def run(self):
        """
        Main orchestrator run loop.
        """
        self.logger.info('=' * 50)
        self.logger.info('AI Employee Orchestrator Starting')
        self.logger.info(f'Vault: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval}s')
        self.logger.info('=' * 50)
        
        # Start filesystem watcher
        self.start_watcher('filesystem', 'filesystem_watcher.py')
        
        # Wait a moment for watcher to initialize
        time.sleep(2)
        
        # Main loop
        try:
            while True:
                self.trigger_claude()
                self.logger.info(f'Next check in {self.check_interval}s')
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.logger.info('Orchestrator stopping...')
        finally:
            self.stop_watchers()
            self.logger.info('Orchestrator stopped')


def main():
    """Parse arguments and run orchestrator."""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Employee Orchestrator')
    parser.add_argument(
        '--vault', '-v',
        default=None,
        help='Path to Obsidian vault (default: parent of scripts folder)'
    )
    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=300,
        help='Check interval in seconds (default: 300)'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run once and exit (no loop)'
    )
    
    args = parser.parse_args()
    
    # Determine vault path
    if args.vault:
        vault_path = args.vault
    else:
        vault_path = Path(__file__).parent.parent
    
    if args.once:
        # Run once (for testing)
        orchestrator = Orchestrator(str(vault_path), args.interval)
        orchestrator.trigger_claude()
    else:
        # Run continuously
        orchestrator = Orchestrator(str(vault_path), args.interval)
        orchestrator.run()


if __name__ == '__main__':
    main()
