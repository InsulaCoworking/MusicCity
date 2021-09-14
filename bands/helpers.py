import os
import re
import uuid

import datetime

from django.db.models import Q
from django.utils.deconstruct import deconstructible

# Random name generator to avoid file overwrites
@deconstructible
class RandomFileName(object):
    def __init__(self, path):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _, filename):
        # @note It's up to the validators to check if it's the correct file type in name or if one even exist.
        extension = os.path.splitext(filename)[1]
        return self.path % (uuid.uuid4(), extension)


LATENIGHT_HOURS = datetime.time(5, 0, 0)
def order_latenight(event_a, event_b):
    if event_a.time == event_b.time:
        return 0
    elif event_a.time < LATENIGHT_HOURS:
        if event_b.time < LATENIGHT_HOURS:
            return -1 if event_a.time < event_b.time else 1
        else:
            return -1
    elif event_b.time < LATENIGHT_HOURS:

        return -1
    else:
        return -1 if event_a.time < event_b.time else 1

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):

    '''
    Splits the query string in invidual keywords, getting rid of unecessary spaces and grouping quoted words together.
    Example:
    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''

    return [normspace('', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):

    '''
    Returns a query, that is a combination of Q objects.
    That combination aims to search keywords within a model by testing the given search fields.
    '''

    query = None  # Query to search for every search term
    terms = normalize_query(query_string)

    for term in terms:
        if len(term)<3:
            continue
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query

    return query


socialnetwork_urls = {
    'instagram': 'https://www.instagram.com/{}/',
    'twitter': 'https://twitter.com/{}/',
    'facebook': 'https://www.facebook.com/{}',
    'bandcamp': 'https://{}.bandcamp.com/',

}

def get_url_for_social_network(url_or_username, page):
    if url_or_username and url_or_username.startswith('http'):
        return url_or_username

    if page in socialnetwork_urls:
        username = url_or_username[1:] if url_or_username.startswith('@') else url_or_username
        return socialnetwork_urls[page].format(username)
    else:
        return url_or_username
