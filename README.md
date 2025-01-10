# yt-id-extractor-python
Used for extracting Youtube video IDs from file names that were created by yt-dlp.
This has only been tested for the default configuration given by yt-dlp; regex still needs to be implemented.

The script outputs the video IDs into text files.
batch-a.txt is generated from files that contained only audio.
batch-v.txt is generated from files that at least contained video, whether they had audio or not.
The Python bindings for ffmpeg which allow easy probing for codecs are given by https://pypi.org/project/ffmpeg-python/.

By doing this, one can run yt-dlp with the switch ```-a batch-v.txt``` to re-download the videos referenced by the IDs in the file. This is of course useful if a different quality, or other data is needed for a set of given videos.
