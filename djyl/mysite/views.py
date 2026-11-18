from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from threading import Lock

from .yolo.video_stream import generate_frames


MEDICINE_INFORMATION = {
    "augmentin": {
        "family": "Antibiotic — penicillin / beta-lactam combination",
        "role": "Kills susceptible bacteria by preventing bacterial cell-wall synthesis.",
        "diseases": "Respiratory tract infections, ear infections, sinusitis and urinary tract infections.",
        "usage": "Take exactly as prescribed, preferably at the start of a meal. Complete the full course.",
    },
    "celebrex": {
        "family": "Anti-inflammatory — COX-2 selective inhibitor",
        "role": "Reduces pain and inflammation.",
        "diseases": "Arthritis, joint pain and acute inflammatory pain.",
        "usage": "Use the lowest effective dose for the shortest time prescribed by a healthcare professional.",
    },
    "chlort": {
        "family": "Antibiotic — tetracycline",
        "role": "Stops bacteria from producing essential proteins.",
        "diseases": "Certain bacterial skin, eye and respiratory infections.",
        "usage": "Apply or take only according to the prescription. Avoid use with dairy or antacids unless advised.",
    },
    "methylprednisolone": {
        "family": "Corticosteroid",
        "role": "Controls inflammation and suppresses abnormal immune activity.",
        "diseases": "Severe allergic reactions, inflammatory disorders and autoimmune conditions.",
        "usage": "Administer strictly as prescribed; do not stop an injection or course abruptly.",
    },
    "paracetamol": {
        "family": "Analgesic and antipyretic",
        "role": "Relieves mild-to-moderate pain and reduces fever.",
        "diseases": "Headache, fever, dental pain and muscle aches.",
        "usage": "Use as directed on the label or by a clinician. Do not exceed the maximum daily dose.",
    },
    "phloroglucinol": {
        "family": "Smooth-muscle antispasmodic",
        "role": "Relaxes smooth muscles and reduces painful spasms.",
        "diseases": "Abdominal, urinary or gynecological spasms.",
        "usage": "Take only as directed by a healthcare professional and when an acute spasm occurs.",
    },
    "prednisolone": {
        "family": "Corticosteroid",
        "role": "Reduces inflammation and modifies immune-system activity.",
        "diseases": "Asthma, allergies, inflammatory diseases and some autoimmune conditions.",
        "usage": "Follow the prescribed dose and schedule carefully; tapering may be required.",
    },
    "metronidazole": {
        "family": "Antibiotic and antiprotozoal",
        "role": "Damages DNA in susceptible bacteria and parasites.",
        "diseases": "Bacterial vaginosis, amoebiasis and some intestinal or dental infections.",
        "usage": "Take at the times prescribed and complete the course. Avoid alcohol during treatment unless a clinician approves.",
    },
}

_detection_lock = Lock()
_latest_detection = {"name": None, "confidence": 0}


def _clean_name(name):
    if not name:
        return None
    try:
        return name.encode("latin1").decode("utf8").strip()
    except (UnicodeEncodeError, UnicodeDecodeError):
        return name.strip()


def _medicine_key(name):
    name = _clean_name(name)
    normalized = (name or "").lower().replace("é", "e").replace("è", "e").replace("â", "a")
    for key in MEDICINE_INFORMATION:
        if key in normalized:
            return key
    if "meth" in normalized and "prednisolone" in normalized:
        return "methylprednisolone"
    return None


def video_feed(request):
    def detection_callback(name, confidence):
        global _latest_detection
        name = _clean_name(name)
        key = _medicine_key(name)
        information = MEDICINE_INFORMATION.get(key)
        payload = {
            "name": name,
            "confidence": round(confidence * 100, 1),
            "family": information["family"] if information else "Medicine information not available",
            "role": information["role"] if information else "Consult a healthcare professional for identification.",
            "diseases": information["diseases"] if information else "Not available in the local medicine catalogue.",
            "usage": information["usage"] if information else "Do not use until a pharmacist or doctor confirms the medicine.",
        }
        with _detection_lock:
            _latest_detection = payload

    return StreamingHttpResponse(
        generate_frames(source=0, detection_callback=detection_callback),
        content_type="multipart/x-mixed-replace; boundary=frame",
    )


def detection_info(request):
    with _detection_lock:
        payload = dict(_latest_detection)
    return JsonResponse(payload)


def video_page(request):
    return render(request, "mysite/video.html")
