from django.contrib.syndication.views import Feed
from models import *
from rss10 import RDFRSSFeed, RDFXMLFeed

class PostFeed(Feed):
    title = "Post news"
    link = "/rss/"
    description = "Updates on changes and additions to ."

    #description_template

    def items(self):
        return Post.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content
        
class RDFPostFeed(PostFeed):
    feed_type = RDFRSSFeed

    def item_extra_kwargs(self, item):
        return {'content_encoded': self.item_content_encoded(item),
                'privacy': self.item_privacy(item),
                'uri': self.item_uri(item)}

    def item_uri(self, item):
        return str(item.uri())

    def item_content_encoded(self, item):
        content = item.rdf()
        return content
    
    def item_privacy(self, item):
        return "this will be privacy"

class XMLPostFeed(PostFeed):
    feed_type = RDFXMLFeed
