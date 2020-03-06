# ffmpeg-multi-threaded-convert
It will scan a directory and its sub-directories for video files, and if the codecs are not AAC/H264, it will convert them to meet the codecs criteria.

```
usage: ffmpeg_mt.py [-h] -d DIRECTORY -o OUTPUT [-O {yes,no}] [-s {yes,no}]
                     [-t THREADS]

ffmpeg multithreaded utility

Required arguments:
  -d DIRECTORY, --directory DIRECTORY
                        Starting directory
  -o OUTPUT, --output OUTPUT
                        Output directory
  -O {yes,no}, --overwrite {yes,no}
                        Overwrite converted files

Optional arguments:
  -s {yes,no}, --silent {yes,no}
                        Show only QUEUES during scan - Default: no
  -t THREADS, --threads THREADS
                        Max parallel convertions - Default: 1
```
### Example syntax:
```python ffmpeg_nt.py --directory "C:\path\to video files" --output "C:\path\to destination directory" --overwrite yes --threads 2```
