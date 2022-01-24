import concurrent.futures
import os.path
import sys
import time
import multiprocessing as mp
from classes import Frame, Effect
from PIL import Image
import numpy, cv2
import matplotlib.pyplot as plt


image_path = "src/resources/787221.jpg"
repeats = 10
total_frames = 100
output_width = 500
output_height = 500

def createAnimatedMP4(path, width, height, animatedImages, fps):
    print(f"[createAnimatedMP4] Generating MP4 video to {path}")
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    # Create the OpenCV VideoWriter
    video = cv2.VideoWriter(path, # Filename
        fourcc, # Negative 1 denotes manual codec selection. You can make this automatic by defining the "fourcc codec" with "cv2.VideoWriter_fourcc"
        fps, # 30FPS and 60FPS is more typical for a YouTube video
        (width,height) # The width and height come from the stats of image1
    )

    # Conversion from PIL to OpenCV from: http://blog.extramaster.net/2015/07/python-converting-from-pil-to-opencv-2.html
    for img in animatedImages:
        video.write(cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR))

    # Release the video for it to be committed to a file
    video.release()
    print(f"[createAnimatedMP4] Done")

def effect_pan(src, effectFrom, effectTo, steps = 1):
    frames = []
    x_steps = round(abs(int(effectFrom.x) - int(effectTo.x)) / steps)
    y_steps = round(abs(int(effectFrom.y) - int(effectTo.y)) / steps)
    for i in range(steps):
        x_step = int(effectFrom.x) + x_steps*i
        y_step = int(effectFrom.y) + y_steps*i
        # print("[effect_pan] Idx [{0}]: steps ({1},{2}), step ({3},{4})".format(i, x_steps, y_steps, x_step, y_step))
        # tempCrop = img.crop((x_step, y_step, x_step+width, y_step+height))
        frames.append(Frame(src, x_step, y_step))
    return frames

def core_logic(index):
    print("==========================")
    print(f"== Iteration {index} of {repeats}")
    print("==========================")
    fromEffect = Effect(0,0,"pan")
    toEffect = Effect(5500,3500,"pan")
    frames = effect_pan(image_path, fromEffect, toEffect, total_frames)
    images = []
    for idx, frame in enumerate(frames):
        outputImg = Image.new("RGBA",(output_width, output_height))
        # plt.figure(figsize=(2, 1))  # 2 row and 1 column.
        
        inputImage = Image.open(os.path.join(".", frame.src))
        # print(f"\t {(frame.x, frame.y, frame.x+output_width, frame.y+output_height)}")
        inputImage = inputImage.crop((frame.x, frame.y, frame.x+output_width, frame.y+output_height))
        # plt.subplot(2, 1, 1), plt.imshow(inputImage)

        outputImg.paste(inputImage, (0,0))
        print(f"\tprocessed image {idx} out of {len(frames)}")
        # plt.subplot(2, 1, 2), plt.imshow(outputImg)

        # plt.show()
        
        images.append(outputImg)
    
    targetpath = os.path.join("output", f"filename_{index}.mp4")

    createAnimatedMP4(targetpath, output_width, output_height, images, 30)
    return index


def main():
    # 100x do the SAME thing...
    for i in range(1,repeats):
        # Step 1: Create an effect to "pan" a large image
        core_logic(i)


def main_multi():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        fake = range(repeats)
        results = executor.map(core_logic, fake)

        for result in results:
            print(f"Done processing: #{result}")


if __name__ == "__main__":
    print(f'You have {mp.cpu_count()} cores')

    print('--------- single core ---------')
    start = time.process_time()
    # main()
    end = time.process_time()

    print(f'It took {round(end-start,2)} secs on 1 core')

    print('--------- multi core ---------')
    start = time.process_time()
    main_multi()
    end = time.process_time()
    print(f'It took {round(end-start,2)} secs on {mp.cpu_count()} cores')

  
