from youtubesearchpython import VideosSearch

videosSearch = VideosSearch("Minecraft",limit = 1)

print(videosSearch.result()['result'][0]['title'])
print(videosSearch.result()['result'][0]['link'])
