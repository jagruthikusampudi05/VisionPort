
# VisionPort

VisionPort is a computer vision project using Python, PyTorch and YOLO for object detection.

## Technologies Used
- Python
- PyTorch
- Ultralytics YOLO
- Streamlit
- FastAPI
- Uvicorn
- Pandas
- Pillow

## Project Structure

```text
VisionPort/
├── data/
├── models/
├── eval/
├── optimise/
├── serve/
│   ├── gateway.py
│   ├── gateway_trace.py
│   └── __init__.py
├── train/
├── logs/
├── docs/
├── failures/
├── app.py
├── main.py
├── env_check.py
├── env_report.md
├── requirements.txt
└── README.md
```

## Environment Setup

Activate the virtual environment:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Verification

Run:

```bash
python env_check.py
```

This generates `env_report.md` with system and package information.

## Git Workflow

- `main` – main development branch
- `feature/env-check` – environment-check feature branch
- `v0.1` – initial project version

## Author

Jagruthi
