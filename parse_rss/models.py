import httplib
from xml.etree import ElementTree

from django.db import models

# Create your models here.


class Feed(models.Model):
    """an object to handle the rss source of a feed"""
    domain = models.CharField(max_length = 200, help_text='ex: amad.ca')
    uri = models.CharField(max_length = 200, help_text="ex: /rss.xml note:this must begin with '/'")
    
    def __unicode__(self):
        return 'http://%s%s' %(self.domain, self.uri)
    
    def update(self):
        conn = httplib.HTTPConnection(self.domain)
        conn.request("GET", self.uri)
        response = conn.getresponse()
        
        if response.status != 200:
            #TODO email support more information?
            raise Exception("Bad response from "+self.domain+self.uri+": "+str(response.status) +" "+ response.reason)
            
        data = response.read()
        
        #print "Data from Server:"
        #print data
        conn.close()
        
        
        tree = ElementTree.fromstring(data)
        
        for item in tree.find('channel').findall('item'):
            guid = item.find('guid').text
            title = item.find('title').text
            link = item.find('link').text
            description = item.find('description').text
            pubDate = item.find('pubDate').text
            
            article, created = Article.objects.get_or_create(
                    feed = self,
                    guid = guid, 
                    defaults={
                        'title': title,
                        'link': link,
                        'description': description,
                        'pubDate': pubDate,
                    }
                )
            if not created:
                #check fields for changes, and update if necessary
                changed = False
                if article.title != title:
                    article.title = title
                    changed = True
                if article.link != link:
                    article.link = link
                    changed = True
                if article.description != description:
                    article.description = description
                    changed = True
                if article.pubDate != pubDate:
                    article.pubDate = pubDate
                    changed = True
                if changed:
                    article.save()
            


class Article(models.Model):
    """ storage location for feed posts"""
    
    feed = models.ForeignKey(Feed, related_name='articles')
    created = models.DateTimeField(auto_now_add = True)
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    guid = models.CharField(max_length=255)
    pubDate = models.CharField(max_length=100)
    
    def __unicode__(self):
        return '%s' % self.title
        
    class Meta:
        get_latest_by = 'created'
    
    
