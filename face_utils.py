import cv2
import numpy as np
import mediapipe as mp
from sklearn.metrics.pairwise import cosine_similarity

class FaceRecognizer:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)
        self.face_mesh = self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=10, min_detection_confidence=0.5)
    
    def get_face_encoding(self, image):
        """Extract face encoding from image"""
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_image)
        
        if not results.multi_face_landmarks:
            return None
        
        # Get first face landmarks
        landmarks = results.multi_face_landmarks[0]
        
        # Extract key landmark coordinates as encoding
        encoding = []
        for landmark in landmarks.landmark:
            encoding.extend([landmark.x, landmark.y, landmark.z])
        
        return np.array(encoding)
    
    def detect_faces(self, image):
        """Detect faces and return locations"""
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_image)
        
        face_locations = []
        if results.detections:
            h, w, _ = image.shape
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                
                # Convert to (top, right, bottom, left) format
                top = max(0, y)
                left = max(0, x)
                bottom = min(h, y + height)
                right = min(w, x + width)
                
                face_locations.append((top, right, bottom, left))
        
        return face_locations
    
    def get_face_encodings(self, image, face_locations):
        """Get encodings for detected faces"""
        encodings = []
        for (top, right, bottom, left) in face_locations:
            face_img = image[top:bottom, left:right]
            if face_img.size == 0:
                continue
            encoding = self.get_face_encoding(face_img)
            if encoding is not None:
                encodings.append(encoding)
        
        return encodings
    
    def compare_faces(self, known_encodings, face_encoding, tolerance=0.85):
        """Compare face encoding with known encodings"""
        if len(known_encodings) == 0:
            return []
        
        similarities = cosine_similarity([face_encoding], known_encodings)[0]
        matches = similarities > tolerance
        return matches.tolist()
    
    def face_distance(self, known_encodings, face_encoding):
        """Calculate distance between face encodings"""
        if len(known_encodings) == 0:
            return np.array([])
        
        similarities = cosine_similarity([face_encoding], known_encodings)[0]
        distances = 1 - similarities
        return distances
    
    def release(self):
        """Release resources"""
        self.face_detection.close()
        self.face_mesh.close()
