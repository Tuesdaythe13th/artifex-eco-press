import cv2
import numpy as np
import logging
from typing import Tuple

logger = logging.getLogger("VisionScanner")

class DefectScanner:
    def __init__(self, haze_threshold: int = 40, min_flash_area: int = 50):
        self.haze_threshold = haze_threshold
        self.min_flash_area = min_flash_area

    def audit_disc(self, image_path: str) -> Tuple[float, bool]:
        """
        Scans a disc image for haze and flash defects.
        Returns:
            Tuple containing:
            - haze_score (float): 0.0 (perfect) to 1.0 (failed)
            - flash_detected (bool): True if perimeter flash is found
        """
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            logger.error(f"Failed to load image: {image_path}")
            return 1.0, True

        # 1. Flash Detection (Contour perimeter check)
        _, thresh = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        flash_detected = False
        if contours:
            # Assume largest contour is the disc
            largest_contour = max(contours, key=cv2.contourArea)
            # Find deviations from perfect circle
            (x, y), radius = cv2.minEnclosingCircle(largest_contour)
            circle_area = np.pi * (radius ** 2)
            contour_area = cv2.contourArea(largest_contour)
            
            # If contour area significantly deviates from enclosing circle, we have flash
            if circle_area - contour_area > self.min_flash_area:
                flash_detected = True

        # 2. Haze Detection (Laplacian variance proxy for clarity)
        # Low variance means blurry/hazy, high variance means sharp edges (grooves visible)
        laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
        haze_score = 1.0 - min(1.0, laplacian_var / 1000.0)

        if laplacian_var < self.haze_threshold:
            logger.warning(f"Haze detected! Score: {haze_score:.2f}")

        return haze_score, flash_detected
