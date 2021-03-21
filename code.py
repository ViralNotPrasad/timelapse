import cv2 as cv
import numpy as np
import time
import glob
from datetime import datetime
import os
import moviepy.video.io.ImageSequenceClip

def main():
	camera = cv.VideoCapture(2) #replace 2 with 0 if you are using your default webcam, 2 is for external webcam.
	cv.namedWindow("timelapse")
	img_counter = 0
	while True:
		today = datetime.now()
		todayy = today.strftime("%d_%b, %H:%M")
		ret,frame = camera.read()
		if not ret:
			print("failed to grab frame")
			break
		k = cv.waitKey(1)
		if k%256 == 27:
			print("ESC hit, closing..")
			stitch_video()
			break
		time.sleep(5) #no of seconds to wait for
		img_name = "{}_frame{}.png".format(todayy, img_counter) #filename for img

		# org = (325, 475) 
		org = (0,30)
		font = cv.FONT_HERSHEY_SIMPLEX 
		fontt = 1
		color = (0,0,255)
		thickness = 1

		cv.putText(frame, todayy, org, font, fontt,  
                 color, thickness, cv.LINE_AA, False) 

		cv.imwrite(img_name, frame)
		print("{} done".format(img_counter))
		img_counter+=1
	
	camera.release()

	cv.destroyAllWindows()
	
def stitch_video():
	today = datetime.now()
	todayy = today.strftime("%d_%b || %H:%M")
	image_folder = '/home/viralnotprasad/Desktop/timelapse'
	fps=12
	image_files = [image_folder+'/'+img for img in sorted(os.listdir(image_folder),key=os.path.getmtime) if img.endswith(".png")]
	print(type(image_files))
	clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
	vid_name = "{}_video.mp4".format(todayy)
	clip.write_videofile(vid_name)
	time.sleep(1)
	for f in os.listdir(image_folder):
		if f.endswith(".png"):
			os.remove(os.path.join(image_folder, f))

if __name__ == "__main__":
	main()
