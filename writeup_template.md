## Advanced Lane Finding Project

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./examples/undistort.png "Undistorted"
[image2]: ./output_images/test_undist_img.jpg "Road Transformed"
[image3]: ./examples/binary.png "Binary Example"
[image4]: ./examples/binary_warped.png "Warp Example"
[image5]: ./examples/color_fit_lines.jpg "Fit Visual"
[image6]: ./examples/detect_lane.png "Output"  
[image7]: ./examples/lane_detect.png "Lane detect histogram"
[image8]: ./examples/plot.png "Plot"  
 
### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the first code cell of the IPython notebook located in "P4.ipynb".  

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![alt text][image1]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
  
  
* Apply `cv2.undistort` with the camera matrix and distortion coefficients obtained in Camera Calibration Step. 

![alt text][image2]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

By converting the undistorted image to HLS color space and separate the S channel we can see that the S channel is doing a fairly robust job of picking up the lines under very different color and changing conditions, while the other selections look messy. I used a combination of color and gradient thresholds to generate a binary image . Here's an example of my output for these steps.  (note: this is not actually from one of the test images)

 * Grayscale image.
 * Take sobel x gradients.
 * Threshold x gradient and color channel.
 * Stack each channel to view their individual contributions in green and blue respectively.This returns a stack of the two binary images, whose       components you can see as different colors.
 * Combine the two binary thresholds.

![alt text][image3]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform is contained in the fourth code cell of the IPython notebook located in "P4.ipynb".  The `M = cv2.getPerspectiveTransform()` takes as source (`src`) and destination (`dst`) points.  I chose the hardcode the source and destination points in the following manner:

  * Obtain the matrix `M` that maps them to each other using `cv2.getPerspective`.
  * Warp the image to the new birds-eye-view perspective using `cv2.warpPerspective` and the perspective transform matrix `M`
  * Transform the image from the car camera's perspective to a birds-eye-view perspective.

This resulted in the following source and destination points:

Src Points:  
```python
[  190.   720.]
[  589.   457.]
[  698.   457.]
[ 1145.   720.]
```
Dst Points:  
```python
 [  325.  720.]
 [  325.    0.]
 [ 1010.    0.]
 [ 1010.  720.]
```

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image4]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Then I did some other stuff and fit my lane lines with a 2nd order polynomial kinda like this with following steps:  

  * Take a histogram of the bottom half of the image.
  * Find the peak of the left and right halves of the histogram.
  * Choose the number of sliding windows and Set height of windows.
  * Identify the x and y positions of all nonzero pixels in the image.
  * Current positions to be updated for each window.
  * Set the width of the windows +/- margin and minimum number of pixels found to recenter window.
  * Create empty lists to receive left and right lane pixel indices.
  * Step through the windows one by one.
  * Fit a second order polynomial to each lane line using np.polyfit.
  * Generate a polygon to illustrate the search window area and recast the x and y points into usable format for `cv2.fillPoly()`.
  * Draw the lane onto the warped blank image.

![alt text][image5]
![alt text][image7]
![alt text][image8]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

The code for calculated the radius of curvature of the lane and the position of the vehicle is contained in the sixth code cell of the IPython notebook located in "P4.ipynb".  
       
  * Calculated the radius of curvature:  
  `
  right_curverad = ((1 + (2*right_fit_cr[0]*y_eval*ym_per_pix + right_fit_cr[1])**2)**1.5) / np.absolute(2*right_fit_cr[0])`
  `
  * The position of the vehicle:  
  `
  position_from_center = ((x_left_pix + x_right_pix)/2 - midx) * xm_per_pix
  `  
  

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented these steps in the 7th code cell of the IPython notebook located in "P4.ipynb":  
   
 * Create an image to draw the lines on.
 * Recast the x and y points into usable format for `cv2.fillPoly()`.
 * Draw the lane onto the warped blank image.
 * Warp the blank back to original image space using inverse perspective matrix (Minv) `cv2.warpPerspective()`.
 * Combine the result with the original image `cv2.addWeighted()`.
 
Here is an example of my result on a test image:

![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).
To smooth the output, updating curvature and polynomials using weighted average with last frame of previously detected lines in the `video_pipeline` function. Here's a [link to my video result](https://www.youtube.com/watch?v=k2YmlkGPopU).

```python
from moviepy.editor import VideoFileClip

output = 'Test.mp4'
clip1 = VideoFileClip("project_video.mp4")
output_clip = clip1.fl_image(video_pipeline)

%time output_clip.write_videofile(output, audio=False)
```


---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Warp the image to the birds-eye-view perspective and fitting lane lines by polynomial is a promising method which may find not only straight lane lines but also curved ones although it's not robust enough to deal with complex environment like the Valley Track in the Behavior cloning project such as shadow, brightness, traffic signs, white lane line with a bright background, appearing, for example, under trees, may lead to noisy results. By applying HLS and sobel masks to the image, I want to have better results but additional issues could happen due to poor condition of road marking, intersection of different lines and as you can see in the challenge.mp4. A fix for that could be checking the distance between the two detected lane lines. Filtering out lines if they are not the correct distance apart like 3.7 meters, will filter out other lines like those in the challenge video may partly be resolved by additional line filtering between video frames. I would like to implement video filtering methods to make it more robust on the harder_challenge_video.mp4 as the future work
