from django.http import StreamingHttpResponse
from django.shortcuts import render
from .yolo.video_stream import generate_frames

def video_feed(request):
    """Stream YOLO detection from webcam."""
    return StreamingHttpResponse(generate_frames(source=0), 
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def video_page(request):
    return render(request, 'mysite/video.html')
