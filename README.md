# TuneTransfer
A Python app to convert my YouTube playlist of videos/music into a ZIP of MP3s so I can easily transfer to my phone.

1. Pull the first 50 videos on YouTube playlist
2. Compare video IDs with "already downloaded" list; if exists, skip
3. Take rest of video IDs and download MP3s
4. Compress to ZIP
5. Save video IDs to already downloaded list
5. Open up Finder and Sharedrop.io