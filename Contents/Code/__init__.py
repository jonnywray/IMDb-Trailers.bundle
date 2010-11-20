
PLUGIN_PREFIX = "/video/IMDBTrailers"

TRAILERS     = "http://www.imdb.com/features/video/trailers"
CONTENT_URL  = "http://www.imdb.com/video/trailers/data/_json?list=%s"
DETAILS_PAGE = "http://www.imdb.com/video/imdb/%s/html5"

SORT_POPULAR = "popular"
SORT_RECENT  = "recent"

SORT_PREFS_KEY = "sortOrder"

CACHE_TIME = 3600


####################################################################################################
def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, "IMDb HD Trailers", "icon-default.png", "art-default.jpg")
  Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.title1 = L('IMDb HD Trailers')
  MediaContainer.art = R('art-default.jpg')
  HTTP.CacheTime = CACHE_TIME

####################################################################################################
def MainMenu():
    dir = MediaContainer(viewGroup='List')
    dir.Append(Function(DirectoryItem(HDVideos, title="Recent HD Trailers"), sort="recent"))
    dir.Append(Function(DirectoryItem(HDVideos, title="Popular HD Trailers"), sort="popular"))
    return dir

####################################################################################################
def HDVideos(sender, sort):
  dir = MediaContainer(viewGroup='Details')
  contentUrl = CONTENT_URL % sort
  content = JSON.ObjectFromURL(contentUrl)
  for video in content['videos']:
    videoId = video['video']
    thumb = video['poster']
    title = video['title_title']
    duration = 1000*int(video['duration_seconds'])
    titleData = HTML.ElementFromString(video['title_data'])
    summary = None
    if len(titleData.xpath('//div[@class="t-o-d-text-block t-o-d-plot"]/span')) > 0:
        summary = titleData.xpath('//div[@class="t-o-d-text-block t-o-d-plot"]/span')[0].text
    
    rating = None
    if len(titleData.xpath('//span[@class="t-o-d-rating-value"]')) > 0:
   	    rating = titleData.xpath('//span[@class="t-o-d-rating-value"]')[0].text
    tagLine = None
    if len(titleData.xpath('//div[@class="t-o-d-text-block t-o-d-tagline"]')) > 0:
   	    tagLine = titleData.xpath('//div[@class="t-o-d-text-block t-o-d-tagline"]/span')[0].text
    Log("Adding video item:"+title)
    
    dir.Append(Function(VideoItem(PlayVideo, title=title, summary=summary, subtitle=tagLine, rating=rating, thumb=thumb, duration=duration), videoId = videoId))
  return dir


####################################################################################################
# TODO: expand content by parsing TRAILERS, although the above seems to be their way ahead
def Videos(sender):
    dir = MediaContainer(viewGroup='Details')
    return dir
    
####################################################################################################
def PlayVideo(sender, videoId):
    detailsUrl = DETAILS_PAGE % (videoId)
    Log("DetailsURL:"+detailsUrl)
    details = HTTP.Request(detailsUrl).content
    index = details.find('mp4_h264')
    start = details.find('http', index)
    end = details.find("'", start)
    videoUrl = details[start:end]
    Log("VideoURL:"+videoUrl)
    return Redirect(videoUrl)