channel1 = 'https://t.me/nefaktiki'
channelID1 = '@nefaktiki'
channel2 = 'https://t.me/+3ZotWW90wl40NDE1'
channelID2 = '@lovgum0'


#tiktok handler
tiktok_url = "https://tiktok-downloader-download-videos-without-watermark1.p.rapidapi.com/media-info/"
tiktok_headers = {
    "X-RapidAPI-Key": "c72e90651emsh8f7d07130d77329p11782fjsn931c2413a109",
    "X-RapidAPI-Host": "tiktok-downloader-download-videos-without-watermark1.p.rapidapi.com"
}


#youtube handler
youtube_url = "https://youtube-media-downloader.p.rapidapi.com/v2/video/details"
youtube_headers = {
    "X-RapidAPI-Key": "c72e90651emsh8f7d07130d77329p11782fjsn931c2413a109",
    "X-RapidAPI-Host": "youtube-media-downloader.p.rapidapi.com"
}


#instagram_handler
instagram_url = 'https://instagram-downloader-download-instagram-videos-stories.p.rapidapi.com/index'
instagram_headers = {
    "X-RapidAPI-Key": "c72e90651emsh8f7d07130d77329p11782fjsn931c2413a109",
    "X-RapidAPI-Host": "instagram-downloader-download-instagram-videos-stories.p.rapidapi.com"
}


#add user to db
async def add_user(user_id, username):
    db.saverusers.insert_one({
        "uid": user_id,
        "username": username,
        "date": int(time.time()),
    })