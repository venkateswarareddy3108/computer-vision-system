"""
Face recognition module.
Re-exports the combined InsightFace provider.
"""

from app.vision.face_detector import InsightFaceProvider

# In our implementation, the detector and recognizer are the same instance
# because InsightFace's FaceAnalysis handles both efficiently in one pass.
FaceRecognizer = InsightFaceProvider
