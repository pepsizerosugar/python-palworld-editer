import os
import sys
import time

MAJOR_UPDATE = 0
RECOMMENDED_UPDATE = 1
PATCH_UPDATE = 2


class Version:
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"


def get_running_directory():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        return os.getcwd()


class VersionChecker:
    def __init__(self):
        self.max_loop_time = 5 * 60
        self.releases = None
        self.current_version = Version(1, 0, 0)
        self.dir_path = get_running_directory()
        self.run_updater()

    def run_updater(self):
        global update_process
        try:
            update_path = os.path.join(self.dir_path, "PalUpdater.exe")
            import subprocess
            update_process = subprocess.Popen(
                [update_path, str(self.current_version)])
            try:
                start_time = time.time()

                while True:
                    if os.path.exists('update_not_needed.txt'):
                        print(f"Update is not needed. Shutting down the updater.")
                        update_process.kill()
                        os.remove('update_not_needed.txt')
                        break

                    if os.path.exists('shutdown_request.txt'):
                        print(f"Shutting down the My Self.")
                        print(f"Wait for killing...")
                        pass

                    if time.time() - start_time > self.max_loop_time:
                        break

                    time.sleep(1)
            except Exception as e:
                print(e)
                pass
        except Exception as e:
            print(e)
            pass
