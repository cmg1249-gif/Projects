import os
import requests
import subprocess
# Downloading Furmark installer from the web 
# 
furmark_url = "https://geeks3d.com/dl/get/831"
INSTALLER_PATH = "furmark_installer.exe"
def download_furmark():
    try:
        print("Downloading Furmark...")
        response = requests.get(furmark_url, stream=True)

        if response.status_code != 200:
            print("Download Failed: HTTP", response.status_code)
            return False
        with open(INSTALLER_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print("Download Completed. Installer saved as", INSTALLER_PATH)
        
        return True
    except Exception as e:
        print("an error occurred during download:", str(e))
        return False




# Checking if Furmark is installed
FURMARK_DIR = r"C:\Program Files\Geeks3D\FurMark2_x64"
FURMARK_EXE = os.path.join(FURMARK_DIR, "furmark_GUI.exe")
def furmark_installed():
    if not os.path.exists(FURMARK_DIR):
        return False
    if not os.path.exists(FURMARK_EXE):
        return False
    return True

# Running FurMark installler if not installed
if furmark_installed():
    print("FurMark is allready installed. Continuing...")
else:
    print("Furmark is not installed. Fetching Download on the web...")
    if download_furmark():
        print("Running Furmark installer...")
        subprocess.run([INSTALLER_PATH, "/S"], check=True)
        print("Furmark installation completed.")
    else:
        print("Failed to download Furmark. Please check your internet connection and try again.")
        exit(1)

# Hand off the benchmark execution to the benchmark script
print("Starting benchmark execution...")
subprocess.run(["python", "benchmark_run.py"], check=True)



