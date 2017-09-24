#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 21:34:44 2017

@author: changhsin-wen
"""

import numpy as np
import cv2

class CameraCalibration():
    
    def __init__(self, imgs, width, height):
        
        self.mtx = None  # Camera Matrix
        self.dist = None  # Distortion Coefficients
        self.size = None  # Image size
        self.width = width  # Width of chessboard
        self.height = height  # Height of chessboard
        self.calibrated = False  # Whether the camera has been calibrated
        objpoints, imgpoints = self.get_all_corners(imgs)
        self.mtx, self.dist = self.calibrate(objpoints, imgpoints)

    # Generate a matrix of x, y, z object points
    def gridspace(self, ):
        
        # Initialise 2D array of zeros, needs to be float to stop OpenCV from complaining
        obj = np.zeros((self.width * self.height, 3)).astype(np.float32)
        
        # For x and y, fill with a grid of ascending values
        obj[:, :2] = np.mgrid[0:self.width, 0:self.height].T.reshape(-1, 2)
        return obj

    # Get the image points and the object points for a single image
    def get_corners(self, img):
        objp = self.gridspace() # Generate 3D object points for chessboard
        
        # Convert to grayscale, using RGB instead of BGR as mpimg uses a RGB format
        grey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # Save size of image for later use
        self.size = grey.shape[::-1]

        # Detect chessboard corners
        ret, corners = cv2.findChessboardCorners(grey, (self.width, self.height), None)
        
        if ret:
            return corners, objp
        else:
            return None, None

    # Get the object and image corners for all images.
    def get_all_corners(self, imgs):
        objpoints = []
        imgpoints = []
        for i, img in enumerate(imgs):
            imgp, objp = self.get_corners(img)
            if imgp is None:
                
                # Warn if image is skipped
                print('Image {} skipped chessboard corners is not fully visible'.format(i))
            else:
                objpoints.append(objp)
                imgpoints.append(imgp)
            
        return objpoints, imgpoints

    # Get camera coefficients
    def calibrate(self, objpoints, imgpoints):
        
        # Calculate the camera matrix and the distortion coefficients. This is what we need in order to undistort
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, self.size, None, None)
        return mtx, dist

    # Apply the distortion coefficients to an image
    def undistort(self, img):
        return cv2.undistort(img, self.mtx, self.dist, None, self.mtx)