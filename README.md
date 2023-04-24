# Camera Measurements
This script uses OpenCV and the Vimba library to perform image processing and measurements on video frames captured by a camera. The script can detect and draw bounding boxes around contours in the image, calculate the length and width of each bounding box, and display area measurements on the video feed.

## Installation
To use this script, you need to have the following libraries installed:

* OpenCV
* Vimba SDK
You can install OpenCV and Vimba SDK using the following commands:

'''
pip install opencv-python-headless
pip install vimba-py
''''

## Usage
Clone the repository to your local machine:

'''
git clone https://github.com/your_username/camera-measurements.git
Connect the camera to your computer and modify the camera ID in the script to match the ID of the camera you are using.
'''

'''
cam = vimba.get_camera_by_id('YOUR_CAMERA_ID_HERE')
''''
Run the script:

'''
python camera_measurements.py
'''

The script will open a window showing the video feed from the camera, with the contours and area measurements displayed on the image. The average width and height of the bounding boxes will be displayed in a separate textbox on the video feed. Press 'q' to exit the program.

License
This project is licensed under the MIT License.
