import ffmpeg
from pathlib import Path
import re



ROOT = Path('./')
regex_pattern = r'.*(-\s*|\s+|\[)(?P<id>([a-zA-Z0-9_-]){11})(\])?( - audio only| - [0-9]{3,4}x[0-9]{3,4})?\.(?P<ext>([a-z0-9])+)$'
VIDEO_CODECS = ["vp9", "av1"]
AUDIO_CODECS = ["opus", "aac"]
VIDEO_EXTENSIONS = {"mkv", "mp4", "webm", "avi"}
AUDIO_EXTENSIONS = {"mp3", "m4a", "webm"}
common_extensions = VIDEO_EXTENSIONS.intersection(AUDIO_EXTENSIONS) 
uncommon_extensions = VIDEO_EXTENSIONS.difference(AUDIO_EXTENSIONS) 
all_extensions = VIDEO_EXTENSIONS.union(AUDIO_EXTENSIONS)





def write_batch(list, name):
    if len(list) > 0:
        with open(name, 'w') as file_write:
            file_write.write('\n'.join(list))


items = []
subdirs = input("Include subdirectories? (y/n): ")
if subdirs == "y":
    items = [item for item in ROOT.rglob("*")]
else:
    items = [item for item in ROOT.iterdir()]


video_list = []
audio_list = []
unknown_list = []
for item in items:
    item_name = item.name
    valid = False
    for ext in all_extensions:
        if ext in item_name:
            valid = True
            break
    if valid == False:
        continue

    matches = re.finditer(regex_pattern, item_name)
    for match in matches:
        match_id = match.groupdict()["id"]
        match_ext = match.groupdict()["ext"]
        if match_ext in common_extensions:
            probe_v = str(ffmpeg.probe(item, select_streams='v'))
            probe_a = str(ffmpeg.probe(item, select_streams='a'))
            is_video = False
            is_audio = False

            for codec in VIDEO_CODECS:
                if codec in probe_v:
                    video_list.append(match_id)
                    is_video = True
                    break
                else:
                    continue
            if is_video == False and match_id not in video_list:
                for codec in AUDIO_CODECS:
                    if codec in probe_a:
                        audio_list.append(match_id)
                        is_audio = True
                        break
                    else:
                        continue
            if is_audio == False and is_video == False:
                unknown_list.append(match_id)
        
        elif match_ext in VIDEO_EXTENSIONS:
            video_list.append(match_id)
        elif match_ext in AUDIO_EXTENSIONS:
            audio_list.append(match_id)
        else:
            unknown_list.append(match_id)


print(video_list)
print(audio_list)
print(unknown_list)
write_batch(video_list, "batchv.txt")
write_batch(audio_list, "batcha.txt")
write_batch(unknown_list, "unknownformats.txt")