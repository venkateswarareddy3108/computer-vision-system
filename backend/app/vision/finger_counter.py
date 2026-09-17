"""
Finger counting logic based on MediaPipe hand landmarks.
"""

from typing import List, Tuple

class FingerCounter:
    """
    Counts extended fingers based on hand landmarks geometry.
    """

    # MediaPipe Hand Landmark Indices
    # 0: WRIST
    # Thumb
    THUMB_CMC = 1
    THUMB_MCP = 2
    THUMB_IP = 3
    THUMB_TIP = 4
    # Index Finger
    INDEX_MCP = 5
    INDEX_PIP = 6
    INDEX_DIP = 7
    INDEX_TIP = 8
    # Middle Finger
    MIDDLE_MCP = 9
    MIDDLE_PIP = 10
    MIDDLE_DIP = 11
    MIDDLE_TIP = 12
    # Ring Finger
    RING_MCP = 13
    RING_PIP = 14
    RING_DIP = 15
    RING_TIP = 16
    # Pinky Finger
    PINKY_MCP = 17
    PINKY_PIP = 18
    PINKY_DIP = 19
    PINKY_TIP = 20

    TIP_IDS = [THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]

    @staticmethod
    def count_fingers(landmarks: List[Tuple[float, float, float]], handedness: str) -> int:
        """
        Count the number of extended fingers given 21 normalized landmarks.
        
        Args:
            landmarks: List of (x, y, z) normalized coordinates.
            handedness: 'Left' or 'Right'
            
        Returns:
            Integer count of extended fingers (0-5).
        """
        if not landmarks or len(landmarks) < 21:
            return 0

        fingers = []

        # Thumb logic: depends on whether it's left or right hand.
        # Check x-coordinates to see if thumb tip is further out than the IP joint
        if handedness == 'Right':
            if landmarks[FingerCounter.THUMB_TIP][0] < landmarks[FingerCounter.THUMB_IP][0]:
                fingers.append(1)
            else:
                fingers.append(0)
        else: # Left hand
            if landmarks[FingerCounter.THUMB_TIP][0] > landmarks[FingerCounter.THUMB_IP][0]:
                fingers.append(1)
            else:
                fingers.append(0)

        # 4 Fingers logic: compare y-coordinates of tip and PIP joint.
        # If tip y is less than PIP y (higher in the image), finger is open.
        for id in range(1, 5):
            tip_id = FingerCounter.TIP_IDS[id]
            pip_id = tip_id - 2 # PIP is always tip_id - 2 for index, middle, ring, pinky
            
            if landmarks[tip_id][1] < landmarks[pip_id][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        return sum(fingers)
