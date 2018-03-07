# bgext-py

Experiments on extracting the background images of cartoons.

## Commands used

This project uses [pipenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
```sh
pip install cv2
pip install numpy
```

## ffmpeg

To extract video between two frames (-vframes takes the number of frames, not the last one):

```
ffmpeg -start_number 1 -vframes 520 -i AT-full-episode.mp4 -vcodec copy -acodec copy AT-frames-1-521.mp4
```
