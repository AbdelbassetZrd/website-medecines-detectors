# MedScan — Medicine Detector

MedScan is a Django and YOLO-based medicine detection application. It uses a webcam to identify supported medicine packaging and displays the medicine's family, role, treated conditions, usage guidance, and confidence level.

## 20-second Demo

[![Download and watch the MedScan demo](demo/medscan-demo2-20s.mp4)](demo/medscan-demo2-20s.mp4)

A direct demo video is also available at: [`demo/medscan-demo2-20s.mp4`](demo/medscan-demo2-20s.mp4)

## Features

- Live webcam medicine detection
- YOLO object detection
- Medicine family and role information
- Common treated conditions and usage guidance
- Detection confidence percentage
- Dark green-and-blue interface
- SQLite database for a simple local setup

## Requirements

- Python 3.11 or newer
- A webcam
- Linux, macOS, or Windows
- Browser with webcam permission support

## Installation

Clone the repository:

```bash
git clone https://github.com/AbdelbassetZrd/website-medecines-detectors.git
cd website-medecines-detectors/djyl
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install django pymysql mysqlclient opencv-python ultralytics torch torchvision
```

For a CPU-only PyTorch installation on Linux or Windows, an alternative is:

```bash
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
python -m pip install ultralytics opencv-python django pymysql mysqlclient
```

Initialize the local database:

```bash
python manage.py migrate
```

## Run the Application

Start the Django development server:

```bash
python manage.py runserver
```

Open:

- http://127.0.0.1:8000/api/live/

Allow camera access in the browser when prompted. Hold a supported medicine package in front of the webcam and keep it inside the camera frame.

## Test the YOLO Model

Verify that the trained model loads successfully:

```bash
python manage.py shell -c 'from ultralytics import YOLO; model = YOLO("mysite/yolo/my_model.pt"); print(model.names)'
```

## Supported Detection Classes

The included model contains these medicine labels:

- Augmentin sachets
- Celebrex comprimés
- Chlortétracycline tube
- Méthylprednisolone injection
- Paracétamol comprimés
- Phloroglucinol comprimés
- Prednisolone comprimés
- Métronidazole comprimés

## Camera Troubleshooting

If no camera appears:

1. Connect or enable the webcam.
2. Allow camera access for `127.0.0.1` in the browser.
3. Close applications that may already be using the camera.
4. Ensure the current Linux user has access to `/dev/video0`.

On Linux, the webcam permission can be checked with:

```bash
ls -l /dev/video0
```

## Medical Disclaimer

MedScan provides general medicine information for demonstration purposes. It does not replace a prescription, diagnosis, pharmacist advice, or medical professional. Always read the package leaflet and follow instructions from a qualified healthcare professional.
