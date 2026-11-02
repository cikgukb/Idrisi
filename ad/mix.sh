#!/bin/bash
# Gabung video + voiceover + SFX + muzik latar (diduck bila VO bercakap).
# Guna: bash ad/mix.sh [ad/vo.mp3]
set -e
cd "$(dirname "$0")"
VID=idrisi-ad-30s.mp4; OUT=idrisi-ad-30s-final.mp4; VO=${1:-vo.mp3}
[ -f sfx.wav ] || python3 sfx.py
if [ -f "$VO" ]; then
  ffmpeg -y -loglevel error -i $VID -i "$VO" -i sfx.wav -i bed.wav -filter_complex "\
[1:a]aresample=48000,adelay=200|200,apad,atrim=0:30,loudnorm=I=-16:TP=-1.5,asplit=2[vo][sc];\
[3:a]volume=0.55[bedr];[bedr][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[bed];\
[2:a]volume=0.55[fx];\
[vo][fx][bed]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart $OUT
else
  echo "Tiada $VO — gabung SFX + muzik sahaja"
  ffmpeg -y -loglevel error -i $VID -i sfx.wav -i bed.wav -filter_complex \
  "[1:a]volume=0.6[fx];[2:a]volume=0.5[bed];[fx][bed]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart $OUT
fi
echo "siap ad/$OUT"
