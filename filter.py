import sys
import dict2rss
sys.path.insert(0, 'feedparser')


import urllib
import feedparser

mapUrlPattern = 'http://maps.googleapis.com/maps/api/staticmap?sensor=false&center=%s&zoom=13&size=600x300&maptype=roadmap&markers=color:blue|label:S|%s'

targetUrl = 'http://partnerapi.funda.nl/feeds/Aanbod.svc/rss/?type=koop&zo=/amsterdam/0-200000/60+woonopp/3+kamers/'

feed = feedparser.parse(urllib.urlopen(targetUrl))

convertedEntries = {}
for e in feed['entries']: 
    address = e.title.replace('Te koop:', '')
    convertedEntries[e.title] = {
        'title': e.title,
        'description': e.summary + '<img src="%s" title="Map"/>' % (mapUrlPattern % (address, address)),
    }
my_feed_data = {
    'title': 'My feed',
    'item': convertedEntries,
    'version':'0.1',
}

d = dict2rss.dict2rss(my_feed_data)
d.PrettyPrint()

