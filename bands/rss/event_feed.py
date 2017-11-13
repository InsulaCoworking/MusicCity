from django.utils.feedgenerator import Rss201rev2Feed


class ExtendedEventRSSFeed(Rss201rev2Feed):
    """
    Create a type of RSS feed that applies the Event RDF: http://web.resource.org/rss/1.0/modules/event/.
    """

    def root_attributes(self):
        attrs = super(ExtendedEventRSSFeed, self).root_attributes()
        # We need to add the event namespace to the XML definition
        attrs['xmlns:ev'] = 'http://purl.org/rss/1.0/modules/event/'
        attrs['xmlns:dc'] = 'http://purl.org/dc/elements/1.1/'
        return attrs

    def add_item_elements(self, handler, item):
        super(ExtendedEventRSSFeed, self).add_item_elements(handler, item)

        if item['ev_startdate'] is not None:
            handler.addQuickElement(u'ev:startdate', item['ev_startdate'])
        if item['ev_location'] is not None:
            handler.addQuickElement(u'ev:location', item['ev_location'])
        if item['dc_subject'] is not None:
            handler.addQuickElement(u'dc:subject', item['dc_subject'])

