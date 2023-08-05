# Spatially-Varying-Blur-Detection-python
python implementation of the paper "Spatially-Varying Blur Detection Based on Multiscale Fused and Sorted Transform Coefficients of Gradient Magnitudes" - cvpr 2017

## brief Algorithm overview
Uses discrete cosine transform coefficients at multiple scales and uses max pooling on the high frequency coefficients to get the sharp areas in an image.

## Quickstart
This library performs Spatially Varying Blur Detection which is can be used in many applications such as Depth of field estimation, Depth from Focus estimation, Blur Magnification, Deblurring etc.

## Installation

To install, run:
`pip install blur-detector`

## Usage:	
```
import blur_detector
import cv2
if __name__ == '__main__':
	img = cv2.imread('image_name', 0)
	blur_map = blur_detector.detectBlur(img, downsampling_factor=4, num_scales=4, scale_start=2, num_iterations_RF_filter=3)

	cv2.imshow('ori_img', img)
	cv2.imshow('blur_map', blur_map)
	cv2.waitKey(0)
```
As easy as that!!

    