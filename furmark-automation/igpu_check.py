import re
import subprocess

# Keywords typically found on integrated GPUs. We intentionally avoid matching
# discrete AMD GPUs (e.g., "Radeon RX") so that systems with a discrete AMD
# card will select it over an iGPU.
IGPU_KEYWORDS = [
    "intel uhd",
    "intel iris",
    "intel hd",
    # Some AMD APUs also show "vega" in their name; leave these if you want
    # to explicitly treat them as integrated GPUs.
    "vega",
]
FURMARK_EXE = r"C:\Program Files\Geeks3D\FurMark2_x64\Furmark.exe"

def get_dedicated_gpu_index():
    results = subprocess.run(
        [FURMARK_EXE, "--gpuinfo"],
        capture_output=True,
        text=True,
        check=False,
    )

    lines = results.stdout.splitlines()

    # Parse FurMark's --gpuinfo output into GPU blocks, e.g.:
    # GPU 0:
    # - name: ...
    # - deviceID: ...
    #
    # This lets us choose based on vendor keywords or device IDs.
    gpus = []
    current = None
    for line in lines:
        match = re.match(r"^GPU\s*([0-9]+):", line.strip(), re.IGNORECASE)
        if match:
            if current:
                gpus.append(current)
            current = (match.group(1), line.strip())
            continue

        if current is not None:
            current = (current[0], current[1] + "\n" + line.strip())

    if current:
        gpus.append(current)

    if not gpus:
        print("No GPUs detected in FurMark output. Defaulting to GPU index 0.")
        return "0"

    print("Detected GPUs (from FurMark --gpuinfo):")
    for idx, info in gpus:
        # Print only the header line for readability.
        first_line = info.splitlines()[0]
        print(f"  [{idx}] {first_line}")

    # If there's only one GPU, just use it.
    if len(gpus) == 1:
        idx, info = gpus[0]
        print(f"Only one GPU detected. Using index {idx}: {info.splitlines()[0]}")
        return idx

    # Prefer an NVIDIA GPU if present (common discrete GPU in hybrid systems).
    for idx, info in gpus:
        info_lower = info.lower()
        if "nvidia" in info_lower or "geforce" in info_lower or "10de" in info_lower:
            print(f"Selected dedicated GPU index (NVIDIA): {idx} ({info.splitlines()[0]})")
            return idx

    # Filter out GPUs that look like integrated graphics.
    non_igpus = [
        (idx, info)
        for idx, info in gpus
        if not any(keyword in info.lower() for keyword in IGPU_KEYWORDS)
    ]

    if non_igpus:
        # Choose the last non-iGPU listed (often the discrete GPU).
        idx, info = non_igpus[-1]
        print(f"Selected dedicated GPU index (non-iGPU): {idx} ({info.splitlines()[0]})")
        return idx

    print("Could not detect a dedicated GPU (all GPUs matched iGPU keywords). Defaulting to index 0.")
    return "0"
