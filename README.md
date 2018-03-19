# bgext-py

The object of this experiment is to achieve automatic background extraction from 2D cartoons.

Though, there might be practical applications of this tool, it is done because I find the problem interesting.

## How to use

test: `pipenv run pytest`
## Subproblems

To achieve the background extraction, the following sub-problems must be solved:

1. Identify background and foreground.
2. Split the video in scenes. A scene in this context is defined as a continuous part of a video where the camera angle is preserved, so a panning movement would not be considered a scene change.
3. Substract the foreground from each frame.
4. Fill the space left from the foreground extraction with a sensible guess.

## Experiments

### 01. Background Change Speed

**Hypothesis**: A change in scene can be identified by a sudden "significant" change in the background of the scene.

A simple approximation to identify these sudden changes is to find the difference between frames of the number of pixels identified either as foreground or background. A difference too high represents in most cases a camera break.




## Commands/tools used

This project uses:
- [pipenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
- opencv2
- colorama
- pytest
- anvil
- tableau

## ffmpeg

To extract video between two points in time:

```
ffmpeg -ss 00:00:00 -i AT-full-episode.mp4 -t 00:00:22 -vcodec copy -acodec copy AT-first-22secs.mp4
```

To extract specific frames (extract 988, 989, 990):

```
ffmpeg -i AT-full-episode.mp4 -vf select='eq(n\,988)+eq(n\,989)+eq(n\,990)' -vsync 0 frames%d.jpg
```
