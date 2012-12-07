import sys
import os
import commands
import cv
import time

# constants
EXTRACTOR_NAME = "01"
OUTPUT_FILENAME = "dataset.svm"

# make timestamp for this extraction
localtime = time.localtime()
timestamp = "%04d%02d%02d_%02d%02d_%02d" % (localtime.tm_year, localtime.tm_mon, localtime.    tm_mday, localtime.tm_hour, localtime.tm_min, localtime.tm_sec)

# get path to images
images_path = sys.argv[1]

# get path to keylogs
keylogs_path = sys.argv[2]

# get path to dictionaries
dicts_path = sys.argv[3]

# get date of capture event to extract from
capture_date = sys.argv[4]

# get downsampling factor
downsmpl_factor = int(sys.argv[5])

# get path to output directory
output_path = sys.argv[6]

# construct keylog filename
keylog_filename = capture_date + "_keylog.txt"

# construct dictionary filename
dict_filename = capture_date + "_dict.txt" 

# construct level 1 output_directory name
output_dirname_level_1 = EXTRACTOR_NAME + "_" + capture_date

# construct level 2 output directory name
output_dirname_level_2 = timestamp + "_args_" + str(downsmpl_factor)

# open key log file
keylog_file = open(keylogs_path + keylog_filename, "r")

# open dictionary file
dict_file = open(dicts_path + dict_filename, "r")

# create level 1 output directory if it doesn't exist
if not os.path.exists(output_path + output_dirname_level_1):
  os.makedirs(output_path + output_dirname_level_1)

# create level 2 output directry if it doesn't exist
if not os.path.exists(output_path + output_dirname_level_1 + "/" + output_dirname_level_2):
  os.makedirs(output_path + output_dirname_level_1 + "/" + output_dirname_level_2)

# redirect following output to the output file
sys.stdout = open(output_path + output_dirname_level_1 + "/" + output_dirname_level_2 + "/" + OUTPUT_FILENAME, 'w')

# create images output directry if it doesn't exist
if not os.path.exists(output_path + output_dirname_level_1 + "/" + output_dirname_level_2 + "/dataset_images"):
  os.makedirs(output_path + output_dirname_level_1 + "/" + output_dirname_level_2 + "/dataset_images")

# created named window in case we want to display stuff
cv.NamedWindow('debug', cv.CV_WINDOW_AUTOSIZE)

# create word list from dictionary
word_list = []
for word in dict_file.readlines():
    word_list.append(word.strip('\n'))

# digest keylog into array of (word, start_time, end_time) 
# tuples using word_list to filter out only the words 
# existing in the dictionary, and which have been "well-typed"

word_timeline = []
word = ""
start_time = ""
end_time = ""
hand_state = 1

for keypress in keylog_file.readlines():
    keylog_entry = keypress.strip('\n').split(",")
    key_symbol = keylog_entry[0]
    key_timestamp = keylog_entry[3]

    if key_symbol.isalpha() and len(key_symbol) == 1:
        if hand_state == 1:
            if not start_time:
                start_time = key_timestamp
            word += key_symbol
            end_time = key_timestamp
        else:
            word = start_time = end_time = ""
    elif key_symbol == 'space':
        if hand_state == 1:
            if word:
                if word in word_list:
                    word_timeline.append((word, start_time, end_time))
        else:
            hand_state = 1
        
        word = start_time = end_time = "" 
    else:
        hand_state = 0
        word = start_time = end_time = ""

# for each word instance in the word timeline we want to 
# cut out the corresponding segment in the video stream, 
# process the segment to form a feature vector, and then 
# write the word number and feature vector to a file

master_frame_list = commands.getoutput("ls " + images_path + capture_date + "/ | grep pgm").split('\n')
master_frame_list_index = 0;

for word_instance in word_timeline:
    word = word_instance[0]
    word_start_time = word_instance[1]
    word_end_time = word_instance[2]
    word_frame_list = []

    while master_frame_list_index < len(master_frame_list):
        frame_name = master_frame_list[master_frame_list_index]
        frame_time = frame_name[2:19]

        if frame_time < word_start_time:
            master_frame_list_index += 1
        elif frame_time <= word_end_time:
            word_frame_list.append(frame_name)
            master_frame_list_index += 1
        else:
            break
    
    if master_frame_list_index >= len(master_frame_list):
        break

    # take frames and make feature vector
    # "let's make lemonade!"

    if word_frame_list:
        # use first frame to work out images sizes
        # for creating the sum matrix
        im = cv.LoadImageM(images_path + capture_date + "/" + word_frame_list[0])
        im = cv.GetSubRect(im, (205, 145, 225, 95))
        cv.ConvertScale(im,im,-1,255)
        cv.Threshold(im, im, 165, 0, cv.CV_THRESH_TOZERO)
        im_downsmpl = cv.CreateMat(im.rows/downsmpl_factor, im.cols/downsmpl_factor, cv.CV_8UC3)
        cv.Resize(im, im_downsmpl) 
        
        sum = cv.CreateMat(im_downsmpl.rows, im_downsmpl.cols, cv.CV_16UC3)
        avg = cv.CreateMat(im_downsmpl.rows, im_downsmpl.cols, cv.CV_8UC3)
        cv.SetZero(sum)
        cv.SetZero(avg)

        cv.Add(im_downsmpl, sum, sum)

        if len(word_frame_list) > 1:
            for frame in word_frame_list[1:]:
                im = cv.LoadImageM(images_path + capture_date + "/" + frame)
                im = cv.GetSubRect(im, (205, 145, 225, 95))
                cv.ConvertScale(im,im,-1,255)
                cv.Threshold(im, im, 165, 0, cv.CV_THRESH_TOZERO)
                im_downsmpl = cv.CreateMat(im.rows/downsmpl_factor, im.cols/downsmpl_factor, cv.CV_8UC3)
                cv.Resize(im, im_downsmpl)
                cv.Add(im_downsmpl, sum, sum)
  
        #cv.ConvertScale(sum, avg, 1.0/len(word_frame_list))
        cv.ConvertScale(sum, avg, 1.0)
 

        print word_list.index(word),
        for i in range(avg.rows):
            for j in range(avg.cols):
                print str(i*avg.cols+j+1) + ":" + str(avg[i,j][0]),

        print '\n',
        
        filename = "%s_%02d.jpg" % (word, word_timeline.index(word_instance))
        cv.SaveImage(output_path + output_dirname_level_1 + "/" + output_dirname_level_2 +     "/dataset_images/" + filename, avg)

