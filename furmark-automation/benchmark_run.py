import os
import subprocess

from igpu_check import get_dedicated_gpu_index

FURMARK_DIR= r"C:\Program Files\Geeks3D\Furmark2_x64"
FURMARK_EXE= os.path.join(FURMARK_DIR, "Furmark.exe")
EXPORT_DIR = r".\Furmark_Benchmarks"

def run_furmark_benchmark():
    os.makedirs(EXPORT_DIR, exist_ok=True) # Ensure export directory exists

    env_gpu_index = os.environ.get("FURMARK_GPU_INDEX")
    if env_gpu_index:
        gpu_index = env_gpu_index
        print(f"Using GPU index from FURMARK_GPU_INDEX: {gpu_index}")
    else:
        gpu_index = get_dedicated_gpu_index()
        print(f"Using GPU index: {gpu_index}")

    print("Running FurMark benchmark...")
    subprocess.run([
        FURMARK_EXE,
        "--gpu-index", gpu_index,
        "--demo", "furmark-gl",
        # Use custom resolution + duration to ensure MSAA and runtime limit are honored.
        "--width", "1920",
        "--height", "1080",
        "--fullscreen",
        "--msaa", "8",
        "--vsync", "0",
        "--benchmark",
        # Ensure benchmark ends after 5 minutes (300000 ms)
        "--duration-ms", "300000",
        "--log-gpu-data",
        "--hw-polling-interval", "500",
        "--log-gpu-data-filename", "gpu_results.csv",
        "--export-dir", EXPORT_DIR,
        "--gpu-monitor-print",
    ], check=True)
    print("Stress test completed. Results exported to: ", EXPORT_DIR)

run_furmark_benchmark()
    