import os
import sys
import platform
import subprocess
from datetime import datetime

import torch
import pandas
import PIL
import fastapi
import streamlit
import ultralytics

report = []

report.append("# VisionPort Environment Report")
report.append(f"Date: {datetime.now()}")
report.append(f"OS: {platform.platform()}")
report.append(f"Python: {sys.version}")
report.append(f"Python Executable: {sys.executable}")

report.append("\n## Package Versions")
report.append(f"PyTorch: {torch.__version__}")
report.append(f"CUDA Version: {torch.version.cuda}")
report.append(f"CUDA Available: {torch.cuda.is_available()}")
report.append(f"Pandas: {pandas.__version__}")
report.append(f"Pillow: {PIL.__version__}")
report.append(f"FastAPI: {fastapi.__version__}")
report.append(f"Streamlit: {streamlit.__version__}")
report.append(f"Ultralytics: {ultralytics.__version__}")

if torch.cuda.is_available():
    report.append(f"GPU: {torch.cuda.get_device_name(0)}")
    x = torch.rand(1000, 1000).cuda()
    report.append(f"GPU Matrix Test: {torch.mm(x, x).shape}")
else:
    report.append("GPU: Not available (CPU mode)")
    x = torch.rand(1000, 1000)
    report.append(f"CPU Matrix Test: {torch.mm(x, x).shape}")

try:
    result = subprocess.run(
        ["nvidia-smi"],
        capture_output=True,
        text=True,
        timeout=10
    )
    report.append("\n## NVIDIA SMI")
    report.append(result.stdout if result.returncode == 0 else "NVIDIA GPU not detected")
except Exception:
    report.append("\n## NVIDIA SMI")
    report.append("NVIDIA tools not available")

with open("env_report.md", "w", encoding="utf-8") as file:
    file.write("\n".join(report))

print("Environment check completed!")
print("Report saved as env_report.md")