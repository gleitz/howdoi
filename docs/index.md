# howdoi
Never have open your browser to look for answers again.

Create tar archive:
```bash
$ howdoi create tar archive
> tar -cf backup.tar --exclude "www/subf3" www
```

Format a date in bash:
```bash
$ howdoi format date bash
> DATE=`date +%Y-%m-%d`
```
Print stack trace in Python:
``` bash
$ howdoi print stack trace python
> import traceback
>
> try:
>     1/0
> except:
>     print '>>> traceback <<<'
>     traceback.print_exc()
>     print '>>> end of traceback <<<'
> traceback.print_exc()
```

Convert MP4 to GIF:
```bash
$ howdoi convert mp4 to animated gif
> video=/path/to/video.avi
> outdir=/path/to/output.gif
> mplayer "$video" \
>         -ao null \
>         -ss "00:01:00" \  # starting point
>         -endpos 10 \ # duration in second
>         -vo gif89a:fps=13:output=$outdir \
>         -vf scale=240:180
```

