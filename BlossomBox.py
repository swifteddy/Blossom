import cv2
import numpy as np
from vimba import *
import time
import cProfile
import os

#def main():
    # Your code here
#==============================================================================#
# Get the path of the cv2 module
print(cv2.__file__)
# Set default thresholding parameters
block_size = 201
C_constant = 40
avg_width = 0
avg_height = 0

with Vimba.get_instance() as vimba:
    vimba._startup()
    cam = vimba.get_camera_by_id('DEV_1AB22C014D73')

    if not cam:
        print("No cameras found!")
        exit()

    with cam:
        # Check if camera is connected and initialized
        frame = cam.get_frame()
        if frame.get_status() != FrameStatus.Complete:
            print("Failed to acquire frame!")
            exit()
        
        # Start continuous acquisition of video frames
        cam.AcquisitionMode.set('Continuous')
        exposure_time = cam.ExposureTime
        exposure_time.set(40000)
        
        # Wait for some time while frames are being acquired
        time.sleep(5)

        # Stop continuous acquisition
        cam.stop_streaming()

        # Create windows to display the video feed and area measurements
        cv2.namedWindow('Video Feed', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Video Feed', 805, 530)

        while True:
            # initialize empty lists
            widths = []
            heights = []
            
            # Get the latest frame from the camera
            frame = cam.get_frame()
            
            # Check if the frame is complete before processing it
            if frame.get_status() != FrameStatus.Complete:
                continue

            # Crop the frame to the ROI
            roi = frame.as_opencv_image()[150:2800, 0:4024]
            
           # Image pre processing
            gray = cv2.cvtColor(roi, cv2.COLOR_BAYER_RG2GRAY)
            blur = cv2.GaussianBlur(gray, (19, 19), 0)
            #dilate = cv2.dilate(blur, (3,3), iterations=1)
            _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            
            # find contours in the thresholded image
            cnts, hierarchy = cv2.findContours(thresh,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)

            
            # Draw the bounding box around each contour and display its length and width
            for c in cnts:
                area = cv2.contourArea(c)
                if area < 2000 or area > 1000000:
                    continue
                
                # calculate the bounding box of the contour
                x, y, w, h = cv2.boundingRect(c)

                # draw the bounding box on the frame
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # calculate l and w of bounding box
                width = w/90
                height = h/95
                area = area/12100

                # append the length and width to the corresponding lists
                widths.append(width)
                heights.append(height)
                
                # display the length and width of the bounding box
                cv2.putText(roi,
                            "{:.2f}cm x {:.2f}cm".format(width, height),
                            (int(x),
                             int(y - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.5, (155, 155, 155),
                            6)
                # display the area of the bounding box
                cv2.putText(roi,
                            "{:.2f}cm^2".format(area),
                            (int(x),
                             int(y - 90)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.5, (155, 155, 155),
                            6)
                
                # compute the average length and width of all the bounding boxes
                if len(widths) > 0:
                    avg_width = sum(widths) / len(widths)
                    avg_height = sum(heights) / len(heights)
                else:
                    avg_width = 0
                    avg_height = 0

            # add a textbox to the video feed window to display the average length and width
            cv2.putText(roi,
                        "Avg Width: {:.2f}cm".format(avg_width),
                        (100, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        2, (0, 255, 0),
                        6, cv2.LINE_AA)

            cv2.putText(roi,
                        "Avg Height: {:.2f}cm".format(avg_height),
                        (100, 200),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        2, (0, 255, 0),
                        6, cv2.LINE_AA)
                
            # Display the video feed with the contours and area measurements
            cv2.imshow('Video Feed', roi)
            
            # Wait for a key press and exit if 'q' is pressed
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        # Release the camera and close the windows
        cam.stop_streaming()
        
    vimba._shutdown()
    cv2.destroyAllWindows()
#==============================================================================#
        
#if __name__ == '__main__':
    #cProfile.run('main()', filename='my_profile_results.txt')
