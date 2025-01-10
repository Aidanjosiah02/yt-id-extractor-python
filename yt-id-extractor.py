# imports
import os
import ffmpeg
import re

# constants (and variables that can be thought of as constants)
regex_pattern = r'.*(-|\[)(?P<id>([a-zA-Z0-9]){11})(\])?\.(?P<ext>([a-z0-9])*)$'
ALLOWED_CHARS = "[a-zA-Z0-9_-]+"
VIDEO_CODECS = ["vp9", "av1"]
AUDIO_CODECS = ["opus"]
VIDEO_EXTENSIONS = {".mkv", ".mp4", ".webm", ".avi"}
AUDIO_EXTENSIONS = {".mp3", ".m4a", ".webm"}
common_extensions = VIDEO_EXTENSIONS.intersection(AUDIO_EXTENSIONS) 
uncommon_extensions = VIDEO_EXTENSIONS.difference(AUDIO_EXTENSIONS) 
all_extensions = VIDEO_EXTENSIONS.union(AUDIO_EXTENSIONS)
URL_OPEN1 = '['
URL_OPEN2 = '-'
URL_OPEN3 = ' '
URL_CLOSE1 = ']'
def url_close2_index(extension_list):
    url_close2_string = None
    for index_list in extension_list:
        url_close2_string = str(index_list)
    return url_close2_string
URL_CLOSE2 = url_close2_index(all_extensions)    # change "url_close2_string" in the definition above to change this.
URL_LENGTH = int(11)
print(all_extensions)

# working directory
file_path_input = input("Enter the path to your files. (ex. C:/<directory>). If current working directory, leave empty: ")
option_subdirectories = input("Do you wish to include subdirectories? (y/n): ")
file_path = ('"' + file_path_input + '"')

# navigate to working directory
correct_file_path = None
try:
    os.chdir(os.path.normpath(file_path))
    correct_file_path = file_path
except IOError:
    if "/" in file_path:
        try:
            file_path.replace("/", "\\")
            correct_file_path = os.path.normpath(file_path)
            os.chdir(correct_file_path)
        except IOError:
            if "\\" in file_path:
                file_path.replace("\\", "/")
                correct_file_path = os.path.normpath(file_path)
                os.chdir(correct_file_path)
print(os.getcwd())

# create list of files and list of sub-directories from working directory
file_list = []
sub_dir_list = []
objects = (os.scandir(correct_file_path))
for entry in objects:
    if entry.is_file():
        file_list.append(entry.name)
    if entry.is_dir():
        sub_dir_list.append(entry.name)
objects.close()

# seperate list of files into 'only audio' or video (may also have audio) using defined constants
# files with common_extensions will be sorted out in order to "probe" its contents (see next block)
video_list = []
audio_list = []
common_list = []
if VIDEO_EXTENSIONS or AUDIO_EXTENSIONS in file_list:
    for index_file in file_list:
        for index_extension in common_extensions:
            if index_extension in index_file:
                common_list.append(index_file)
            else:
                continue
        if index_extension not in index_file:
            for index_extension in VIDEO_EXTENSIONS:
                if index_extension in index_file:
                    video_list.append(index_file)
                else:
                    continue
            for index_extension in AUDIO_EXTENSIONS:
                if index_extension in index_file:
                    audio_list.append(index_file)
                else:
                    continue
else:
    print("no compatible extensions found")
    input("Program will now exit. Developer needs to fix this later. Press enter. ")
    quit()
print(video_list)
# probe for file codecs to determine actual contents
unknown_list = []
for common_file in common_list:
    probe_v = str(ffmpeg.probe(common_file, select_streams='v'))
    probe_a = str(ffmpeg.probe(common_file, select_streams='a')) 
    for index_codec in VIDEO_CODECS:
        if index_codec in probe_v:
            video_list.append(common_file)
        else:
            continue
    if index_codec not in probe_v and common_file not in video_list:
        for index_codec in AUDIO_CODECS:
            if index_codec in probe_a:
                audio_list.append(common_file)
            else:
                unknown_list.append(common_file)
common_list.clear()

# filter possible strings into lists
unprocessed_url_video1 = []
unprocessed_url_video2 = []
unprocessed_url_video3 = []
unprocessed_url_audio1 = []
unprocessed_url_audio2 = []
unprocessed_url_audio3 = []
unknown_video_url = []
unknown_audio_url = []
for index_file in video_list:
    if URL_OPEN1 and URL_CLOSE1 in index_file:
        unprocessed_url_video1.append(index_file[index_file.find(URL_OPEN1) : index_file.find(URL_CLOSE1)+len(URL_CLOSE1)])
    elif URL_OPEN2 and URL_CLOSE2 in index_file:
        unprocessed_url_video2.append(index_file[index_file.find(URL_OPEN2) : index_file.find(URL_CLOSE2)+len(URL_CLOSE2)])
    elif URL_OPEN3 and URL_CLOSE2 in index_file:
        unprocessed_url_video3.append(index_file[index_file.find(URL_OPEN3) : index_file.find(URL_CLOSE2)+len(URL_CLOSE2)])
    else:
        unknown_video_url.append(index_file)
for index_file in audio_list:
    if URL_OPEN1 and URL_CLOSE1 in index_file:
        unprocessed_url_audio1.append(index_file[index_file.find(URL_OPEN1) : index_file.find(URL_CLOSE1)+len(URL_CLOSE1)])
    elif URL_OPEN2 and URL_CLOSE2 in index_file:
        unprocessed_url_audio2.append(index_file[index_file.find(URL_OPEN2) : index_file.find(URL_CLOSE2)+len(URL_CLOSE2)])
    elif URL_OPEN3 and URL_CLOSE2 in index_file:
        unprocessed_url_audio3.append(index_file[index_file.find(URL_OPEN3) : index_file.find(URL_CLOSE2)+len(URL_CLOSE2)])
    else:
        unknown_audio_url.append(index_file)
print(unprocessed_url_video1)
print(unprocessed_url_video2)
print(unprocessed_url_video3)
print(unprocessed_url_audio1)
print(unprocessed_url_audio2)
print(unprocessed_url_audio3)
print(unknown_video_url)
print(unknown_audio_url)
# isolate URL using all possible open/close strings
url_video_list = []
url_audio_list = []
for index_file in unprocessed_url_video1:
    open_string_pos = index_file.index(URL_OPEN1)
    close_string_pos = index_file.index(URL_CLOSE1)
    index_string_len = (close_string_pos - open_string_pos) - len(URL_OPEN1)
    if index_string_len == URL_LENGTH:
        url_video_list.append(index_file[open_string_pos + len(URL_OPEN1): close_string_pos])
    else:
        continue
for index_file in unprocessed_url_video2:
    open_string_pos = index_file.index(URL_OPEN2)
    close_string_pos = index_file.index(URL_CLOSE2)
    index_string_len = (close_string_pos - open_string_pos) - len(URL_OPEN2)
    if index_string_len == URL_LENGTH:
        url_video_list.append(index_file[open_string_pos + len(URL_OPEN2): close_string_pos])
    else:
        continue
for index_file in unprocessed_url_video3:
    open_string_pos = index_file.index(URL_OPEN3)
    close_string_pos = index_file.index(URL_CLOSE2)
    index_string_len = (close_string_pos - open_string_pos) - len(URL_OPEN3)
    if index_string_len == URL_LENGTH:
        url_video_list.append(index_file[open_string_pos + len(URL_OPEN3): close_string_pos])
    else:
        continue
for index_file in unprocessed_url_audio1:
    open_string_pos = index_file.index(URL_OPEN1)
    close_string_pos = index_file.index(URL_CLOSE1)
    index_string_len = (close_string_pos - open_string_pos) - len(URL_OPEN1)
    if index_string_len == URL_LENGTH:
        url_audio_list.append(index_file[open_string_pos + len(URL_OPEN1): close_string_pos])
    else:
        continue
for index_file in unprocessed_url_audio2:
    open_string_pos = index_file.index(URL_OPEN2)
    close_string_pos = index_file.index(URL_CLOSE2)
    index_string_len = (close_string_pos - open_string_pos) - len(URL_OPEN2)
    if index_string_len == URL_LENGTH:
        url_audio_list.append(index_file[open_string_pos + len(URL_OPEN2): close_string_pos])
    else:
        continue
for index_file in unprocessed_url_audio3:
    open_string_pos = index_file.index(URL_OPEN3)
    close_string_pos = index_file.index(URL_CLOSE2)
    index_string_len = (close_string_pos - open_string_pos) - len(URL_OPEN3)
    if index_string_len == URL_LENGTH:
        url_audio_list.append(index_file[open_string_pos + len(URL_OPEN3): close_string_pos])
    else:
        continue

# filter invalid characters from ID. ex. spaces, colons, periods...
valid_video_ids = []
valid_audio_ids = []
false_video_ids = []
false_audio_ids = []
for id in url_video_list:
    if(re.search(ALLOWED_CHARS, id)):
        valid_video_ids.append(id)
    else:
        false_video_ids.append(id)
for id in url_audio_list:
    if(re.search(ALLOWED_CHARS, id)):
        valid_audio_ids.append(id)
    else:
        false_audio_ids.append(id)
print(valid_video_ids)
print(valid_audio_ids)

# write to batch files
if len(url_video_list)!=0:
    with open('batch-v.txt', 'w') as file_write:
        file_write.write('\n'.join(url_video_list))
if len(url_audio_list)!=0:
    with open('batch-a.txt', 'w') as file_write:
        file_write.write('\n'.join(url_audio_list))
file_write.close()