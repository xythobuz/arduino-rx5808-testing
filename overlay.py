#!/usr/bin/env python

import cv2
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg

# -----------------------------------------------------------------------------
# ---------------------------- Begin Configuration ----------------------------
# -----------------------------------------------------------------------------

# In- & Output files
videos = [ "./PICT0002.AVI" ]
dataFile = "./LOG-13.TXT"
outFile = "output-scroll.avi"

# First sync point
sync1Video = 16.0
sync1Data = 36.000

# Second sync point
sync2Video = 1180.0
sync2Data = 926.000

# Video dimensions
videoWidth = 640
videoHeight = 480

# Plot overlay dimensions
plotWidth = 620 # videoWidth - 20
plotHeight = 200
plotDpi = 100

# Plot overlay position
plotOffsetX = int((videoWidth - plotWidth) / 2)
plotOffsetY = videoHeight - plotHeight

# -----------------------------------------------------------------------------
# ----------------------------- End Configuration -----------------------------
# -----------------------------------------------------------------------------

# Open both files to get their FPS
caps = []
fpsAverage = 0.0
completeFrameCount = 0
print("Input files:")
for v in videos:
    print("  --> {}".format(v))
    cap = cv2.VideoCapture(v)
    caps.append(cap)
    fpsAverage += float(cap.get(cv2.CAP_PROP_FPS))
    completeFrameCount += int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fpsAverage /= len(videos)
print("  Average FPS: {:.5}".format(fpsAverage))

# Read data from CSV file
timeList = []
valueList = []
minimumValue = 9999
maximumValue = -1
print("Data file: {}".format(dataFile))
with open(dataFile) as f:
    for l in f:
        time, value = l.split(", ")
        timeList.append(float(time) / 1000.0)
        valueList.append(int(value))
        if int(value) < minimumValue:
            minimumValue = int(value)
        elif int(value) > maximumValue:
            maximumValue = int(value)
print("  Minimum Value: {}".format(minimumValue))
print("  Maximum Value: {}".format(maximumValue))
print("  Start Time: {}".format(timeList[0]))
print("  End Time: {}".format(timeList[-1]))

#maximumValue -= (maximumValue - minimumValue) / 2

if sync1Video < 0:
    sync1Video += completeFrameCount * fpsAverage / 1000
if sync2Video < 0:
    sync2Video += completeFrameCount * fpsAverage / 1000

print("Output file: {}".format(outFile))
print("Sync Points:")
print("  {}s : {}s".format(sync1Video, sync1Data))
print("  {:.5}s : {}s".format(sync2Video, sync2Data))
print("---------------------------------------------------")

# Prepare output video file writer & codec
fourcc = cv2.VideoWriter_fourcc(*'X264')
vOut = cv2.VideoWriter(outFile, fourcc, fpsAverage, (videoWidth, videoHeight))

# Set up plot
fig = plt.figure(figsize = [plotWidth / plotDpi, plotHeight / plotDpi], dpi = plotDpi)
ax = fig.add_subplot(1, 1, 1)
fig.tight_layout()
canvas = agg.FigureCanvasAgg(fig)

lastTime = 0
def nearestValueAtTime(t):
    global lastTime
    while ((t < timeList[lastTime]) and (lastTime > 0)):
        lastTime -= 1;
    while ((t > timeList[lastTime]) and (lastTime < (len(timeList) - 1))):
        lastTime += 1;
    return valueList[lastTime]

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

fullCount = 0
fullTime = 0.0
for index in range(len(videos)):
    v = videos[index]
    cap = caps[index]
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = float(cap.get(cv2.CAP_PROP_FPS))
    frameTime = 1.0 / fps
    print("Now processing video \"{}\" with {} frames: {}s @ {:.5} FPS...".format(v, length, length * frameTime, fps))

    for frameCount in range(length):
        ret, frame = cap.read()
        if ret != True:
            print("\nError reading frame!")
            break

        print("\r{}% : {} frames".format(int((frameCount + 1) * 100 / length), frameCount + 1), end = "")

        # Render new plot
        t = translate(fullTime + (frameCount * frameTime), sync1Video, sync2Video, sync1Data, sync2Data)
        ax.cla()
        ax.set_autoscalex_on(False)

        # Always show full plot
        #ax.set_xlim([timeList[0], timeList[-1]])

        # Scrolling plot
        ax.set_xlim([t - 30, t + 30])

        ax.set_autoscaley_on(False)
        ax.set_ylim([minimumValue - 5, maximumValue + 5])
        ax.plot(timeList, valueList, color = "green")
        ax.axvline(t, color = "blue")
        ax.plot([t], [nearestValueAtTime(t)], 'r.', markersize = 10.0)
        canvas.draw()
        plotImage = canvas.get_renderer().tostring_rgb()

        # Blit plot onto video frame
        for i in range(plotWidth):
            for j in range(plotHeight):
                plotPixelR = plotImage[3 * (i + (j * plotWidth))]
                plotPixelG = plotImage[3 * (i + (j * plotWidth)) + 1]
                plotPixelB = plotImage[3 * (i + (j * plotWidth)) + 2]
                plotPixel = [ plotPixelB, plotPixelG, plotPixelR ]
                frame[j + plotOffsetY, i + plotOffsetX] = plotPixel

        vOut.write(frame)

    print()
    fullCount += length
    fullTime += length * frameTime
    cap.release()

print("Finalizing output file...")
vOut.release()

