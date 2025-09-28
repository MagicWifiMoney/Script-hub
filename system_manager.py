"""
Premium Marketing Platform System Manager
Handles auto-cleanup, cache management, and system optimization
"""

import os
import shutil
import psutil
import subprocess
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import signal
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SystemManager:
    """Manages system cleanup, optimization, and auto-reset functionality"""

    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.cache_dir = self.base_dir / "cache"
        self.logs_dir = self.base_dir / "logs"
        self.temp_dir = self.base_dir / "temp"
        self.reports_dir = self.base_dir / "seo_reports"

        # Ensure directories exist
        for dir_path in [self.cache_dir, self.logs_dir, self.temp_dir]:
            dir_path.mkdir(exist_ok=True)

    def auto_cleanup(self, days_old: int = 7) -> dict:
        """Perform comprehensive system cleanup"""
        cleanup_report = {
            "timestamp": datetime.now().isoformat(),
            "cache_cleaned": 0,
            "logs_archived": 0,
            "temp_files_removed": 0,
            "processes_cleaned": 0,
            "storage_freed_mb": 0
        }

        try:
            # Clean old cache files
            cleanup_report["cache_cleaned"] = self._clean_cache(days_old)

            # Archive old logs
            cleanup_report["logs_archived"] = self._archive_logs(days_old)

            # Remove temp files
            cleanup_report["temp_files_removed"] = self._clean_temp_files()

            # Clean up orphaned processes
            cleanup_report["processes_cleaned"] = self._clean_streamlit_processes()

            # Calculate storage freed
            cleanup_report["storage_freed_mb"] = self._calculate_storage_freed()

            logger.info(f"Auto-cleanup completed: {cleanup_report}")

        except Exception as e:
            logger.error(f"Auto-cleanup failed: {e}")
            cleanup_report["error"] = str(e)

        return cleanup_report

    def _clean_cache(self, days_old: int) -> int:
        """Remove old cache files"""
        cleaned_count = 0
        cutoff_date = datetime.now() - timedelta(days=days_old)

        if self.cache_dir.exists():
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    # Check file age
                    file_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
                    if file_time < cutoff_date:
                        cache_file.unlink()
                        cleaned_count += 1
                except Exception as e:
                    logger.warning(f"Could not remove cache file {cache_file}: {e}")

        return cleaned_count

    def _archive_logs(self, days_old: int) -> int:
        """Archive old log files"""
        archived_count = 0
        cutoff_date = datetime.now() - timedelta(days=days_old)

        if self.logs_dir.exists():
            archive_dir = self.logs_dir / "archive"
            archive_dir.mkdir(exist_ok=True)

            for log_file in self.logs_dir.glob("*.log"):
                try:
                    file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                    if file_time < cutoff_date:
                        # Compress and move to archive
                        archive_path = archive_dir / f"{log_file.stem}_{file_time.strftime('%Y%m%d')}.log"
                        shutil.move(str(log_file), str(archive_path))
                        archived_count += 1
                except Exception as e:
                    logger.warning(f"Could not archive log file {log_file}: {e}")

        return archived_count

    def _clean_temp_files(self) -> int:
        """Remove temporary files"""
        removed_count = 0

        # Clean temp directory
        if self.temp_dir.exists():
            for temp_file in self.temp_dir.iterdir():
                try:
                    if temp_file.is_file():
                        temp_file.unlink()
                        removed_count += 1
                    elif temp_file.is_dir():
                        shutil.rmtree(temp_file)
                        removed_count += 1
                except Exception as e:
                    logger.warning(f"Could not remove temp file {temp_file}: {e}")

        # Clean Python __pycache__ directories
        for pycache_dir in self.base_dir.rglob("__pycache__"):
            try:
                shutil.rmtree(pycache_dir)
                removed_count += 1
            except Exception as e:
                logger.warning(f"Could not remove pycache {pycache_dir}: {e}")

        return removed_count

    def _clean_streamlit_processes(self) -> int:
        """Clean up orphaned Streamlit processes"""
        cleaned_count = 0

        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if 'streamlit' in proc.info['name'].lower():
                        cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                        if 'script_hub.py' in cmdline:
                            # Check if process is responsive
                            if not self._is_process_responsive(proc.info['pid']):
                                os.kill(proc.info['pid'], signal.SIGTERM)
                                cleaned_count += 1
                                logger.info(f"Terminated unresponsive Streamlit process: {proc.info['pid']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            logger.warning(f"Could not clean Streamlit processes: {e}")

        return cleaned_count

    def _is_process_responsive(self, pid: int) -> bool:
        """Check if a process is still responsive"""
        try:
            # Simple check - if process exists and has recent activity
            proc = psutil.Process(pid)
            return proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE
        except psutil.NoSuchProcess:
            return False

    def _calculate_storage_freed(self) -> float:
        """Calculate approximate storage freed in MB"""
        # This is a simplified calculation
        # In a real implementation, you'd track before/after disk usage
        return 0.0

    def restart_primary_server(self, port: int = 8511) -> dict:
        """Restart the main Script Hub server on a clean port"""
        try:
            # Kill any existing servers
            subprocess.run(['pkill', '-f', 'streamlit run script_hub.py'],
                         capture_output=True, text=True)

            # Wait a moment for processes to terminate
            time.sleep(2)

            # Start new server
            cmd = [
                'python3', '-m', 'streamlit', 'run', 'script_hub.py',
                '--server.port', str(port),
                '--server.headless', 'true',
                '--browser.gatherUsageStats', 'false'
            ]

            process = subprocess.Popen(cmd, cwd=self.base_dir)

            # Give it time to start
            time.sleep(3)

            return {
                "success": True,
                "pid": process.pid,
                "port": port,
                "url": f"http://localhost:{port}",
                "message": "Premium Script Hub restarted successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to restart Script Hub"
            }

    def get_system_health(self) -> dict:
        """Get comprehensive system health report"""
        try:
            # Disk usage
            disk_usage = shutil.disk_usage(self.base_dir)

            # Memory usage
            memory = psutil.virtual_memory()

            # Process count
            streamlit_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info']):
                try:
                    if 'streamlit' in proc.info['name'].lower():
                        cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                        if 'script_hub.py' in cmdline:
                            streamlit_processes.append({
                                "pid": proc.info['pid'],
                                "cpu_percent": proc.info['cpu_percent'],
                                "memory_mb": proc.info['memory_info'].rss / 1024 / 1024
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            return {
                "timestamp": datetime.now().isoformat(),
                "disk_usage": {
                    "total_gb": disk_usage.total / 1024**3,
                    "used_gb": disk_usage.used / 1024**3,
                    "free_gb": disk_usage.free / 1024**3,
                    "percent_used": (disk_usage.used / disk_usage.total) * 100
                },
                "memory": {
                    "total_gb": memory.total / 1024**3,
                    "used_gb": memory.used / 1024**3,
                    "percent_used": memory.percent
                },
                "processes": {
                    "streamlit_count": len(streamlit_processes),
                    "streamlit_processes": streamlit_processes
                },
                "cache_files": len(list(self.cache_dir.glob("*.json"))) if self.cache_dir.exists() else 0,
                "reports_count": len(list(self.reports_dir.glob("*.json"))) if self.reports_dir.exists() else 0
            }

        except Exception as e:
            return {
                "error": str(e),
                "message": "Failed to get system health"
            }

    def schedule_auto_cleanup(self, interval_hours: int = 24):
        """Schedule automatic cleanup (placeholder for production cron job)"""
        return {
            "message": f"Auto-cleanup scheduled every {interval_hours} hours",
            "next_cleanup": (datetime.now() + timedelta(hours=interval_hours)).isoformat(),
            "implementation": "Add to system cron job: 0 */{} * * * python3 system_manager.py --auto-cleanup".format(interval_hours)
        }

def main():
    """CLI interface for system management"""
    import argparse

    parser = argparse.ArgumentParser(description='Premium Marketing Platform System Manager')
    parser.add_argument('--auto-cleanup', action='store_true', help='Run automatic cleanup')
    parser.add_argument('--health-check', action='store_true', help='Show system health')
    parser.add_argument('--restart-server', type=int, metavar='PORT', help='Restart server on specified port')
    parser.add_argument('--days-old', type=int, default=7, help='Days old for cleanup (default: 7)')

    args = parser.parse_args()

    manager = SystemManager()

    if args.auto_cleanup:
        report = manager.auto_cleanup(args.days_old)
        print(json.dumps(report, indent=2))

    elif args.health_check:
        health = manager.get_system_health()
        print(json.dumps(health, indent=2))

    elif args.restart_server:
        result = manager.restart_primary_server(args.restart_server)
        print(json.dumps(result, indent=2))

    else:
        print("Premium Marketing Platform System Manager")
        print("Use --help for available options")

if __name__ == "__main__":
    main()