import cv2
import numpy as np




def analyze(img, m=2, n=2, path=True):
	"""
	This function takes in a stereo image path or 
	an actual cv2 image object, and will split it
	into left and right halves, section each half into
	an mxn grid, and calculate the difference in luminance
	and sharpness between each grid (m, n) in the two 
	halves.
	"""

	if path:
		img = cv2.imread(img)
	
	height = img.shape[0]
	width = img.shape[1]

	# Cut the image in half
	width_cutoff = width // 2
	left_img = img[:, :width_cutoff] # left image
	right_img = img[:, width_cutoff:] # right image

	# section a middle portion of the left image
	# cut in a bit further from the left hand side
	new_x_start = int(left_img.shape[0]*0.15) 
	new_x_end  = int(left_img.shape[0]*0.95)
	new_y_start = int(left_img.shape[1]*0.05)
	new_y_end = int(left_img.shape[1]*0.95)
	left_img = left_img[new_x_start:new_x_end, new_y_start:new_y_end]


	# section a middle portion of the right image
	# cut in a bit further from the right hand side
	new_x_start = int(right_img.shape[0]*0.05)
	new_x_end = int(right_img.shape[0]*0.85)
	new_y_start = int(right_img.shape[1]*0.05)
	new_y_end = int(right_img.shape[1]*0.95)
	right_img = right_img[new_x_start:new_x_end, new_y_start:new_y_end]
	
	# cut up each image into an mxn grid
	left_grids = create_image_grids(left_img, m=m, n=n)
	right_grids = create_image_grids(right_img, m=m, n=n)

	# compare each side's grid, and calculate the difference in each
	# square's (m, n) luminance and sharpness
	luminance_diffs, sharpness_diffs = compare_left_and_right_grids(left_grids, 
	                                                                right_grids)
	# return these two arrays, each should be mxn long (1 diff per grid)
	return luminance_diffs, sharpness_diffs

def create_image_grids(img, m=2, n=2):
	# section the numpy array of the image into m x n 
	tiles = []

	m_width = img.shape[0]//m
	n_height = img.shape[1]//n

	for i in range(0, m):
		for j in range(0, n):
			tile = img[i*m_width:(i+1)*m_width,j*n_height:(j+1)*n_height,:]
			tiles.append(tile)
	return tiles


def compare_left_and_right_grids(left_grid, right_grid):
		luminance_difference = []
		sharpness_difference = []

		unequal_grid_size_msg = "left and right grid sizes do not match!"
		assert len(left_grid) == len(right_grid), unequal_grid_size_msg

		for i in range(len(left_grid)):
				l_diff = abs(luminance(left_grid[i]) - luminance(right_grid[i]))
				luminance_difference.append(l_diff)
				
				s_diff = abs(sharpness(left_grid[i]) - sharpness(right_grid[i]))
				sharpness_difference.append(s_diff)
		return luminance_difference, sharpness_difference

def luminance(img, gamma=1): 
	img = np.power(img, gamma)
	# Luminance values from 
	# http://poynton.ca/notes/colour_and_gamma/GammaFAQ.html#luminance
	weighted_R = .2126*img[:,:,2]
	weighted_G = .7152*img[:,:,1]
	weighted_B = .0722*img[:,:,0]
	return np.mean(weighted_R + weighted_G + weighted_B)	

def sharpness(img):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	return cv2.Laplacian(gray, cv2.CV_64F).var()