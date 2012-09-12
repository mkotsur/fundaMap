ppp
import webapp2
import logging
import sys
import urllib2
import dict2rss

sys.path.insert(0, 'feedparser')
import feedparser


class MainPage(webapp2.RequestHandler):
    def get(self):
		mapUrlPattern = 'http://maps.googleapis.com/maps/api/staticmap?sensor=false&center=%s&zoom=13&size=600x300&maptype=roadmap&markers=color:blue|label:S|%s'

		# /feeds/Aanbod.svc/rss/?type=koop&zo=/amsterdam/0-200000/60+woonopp/3+kamers/
		targetUrl = 'http://partnerapi.funda.nl' + self.request.path_qs

		feed = feedparser.parse(urllib2.urlopen(targetUrl))

		convertedEntries = {}
		for e in feed['entries']:
		    address = e.title.replace('Te koop:', '')
		    convertedEntries[e.title] = {
		        'title': e.title,
                'link': e.link,
		        'description': e.summary + '<img src="%s" title="Map"/>' % (mapUrlPattern % (address, address)),
		    }
		my_feed_data = {
		    'title': 'My feed',
		    'item': convertedEntries,
		    'version':'0.1',
		}

		d = dict2rss.dict2rss(my_feed_data)

		self.response.headers['Content-Type'] = 'application/xml'
		self.response.out.write(d._out())


app = webapp2.WSGIApplication([(r'.*', MainPage)], debug=False)
