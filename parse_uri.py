"""
    ParseUri
    - Original Script by Steven Levithan <stevenlevithan.com>
      http://blog.stevenlevithan.com/archives/parseuri
    - Ported to python by Glen Zangirolami <theglenbot.com>
"""
import re

class ParseUriDict(object):
    """
        Parse URI dictionary for storing URI components
    """
    def __init__(self, **d):
        self.__dict__.update(d)
    def __repr__(self):
        return str(self.__dict__)
        
class ParseUri(object):
    """
        Parse URI components into a readable dictionary
        Usage:
        p = ParseUri()
        p.options['strict_mode'] = True (defaults to false)
        p.parse('http://www.example.com')
    """
    def __init__(self):
        self.options = {
            'strict_mode': False,
            'key': ["source","protocol","authority","userInfo","user","password","host",
                    "port","relative","path","directory","file","query","anchor"],
            'q': {
                'name':"queryKey",
                'parser': '(?:^|&)([^&=]*)=?([^&]*)'
             },
            'parser': {
                "strict": "^(?:([^:\/?#]+):)?(?:\/\/((?:(([^:@]*)(?::([^:@]*))?)?@)?([^:\/?#]*)(?::(\d*))?))?((((?:[^?#\/]*\/)*)([^?#]*))(?:\?([^#]*))?(?:#(.*))?)",
                "loose": "(?:(?![^:@]+:[^:@\/]*@)([^:\/?#.]+):)?(?:\/\/)?((?:(([^:@]*)(?::([^:@]*))?)?@)?([^:\/?#]*)(?::(\d*))?)(((\/(?:[^?#](?![^?#\/]*\.[^?#\/.]+(?:[?#]|$)))*\/?)?([^?#\/]*))(?:\?([^#]*))?(?:#(.*))?)"       
            }
        }
        self.uri = {}

    def parse_query(self, match):
        """
            Function for replacing strings found in the query pattern
        """
        if match.group(1):
            self.uri[self.options['q']['name']][match.group(1)] = match.group(2)     
            
    def parse(self, string=''):
        """
            Main parsing function, takes one argument (uri)
        """
        o = self.options
        exp = o['parser']['strict'] if o['strict_mode'] else o['parser']['loose'] 

        pattern = re.compile(exp, re.IGNORECASE)
        m = pattern.search(string)
        
        for i in range(0,14):
            self.uri[o['key'][i]] = m.group(i)
        
        self.uri[o['q']['name']] = {}
        
        if self.uri['query']:
            pattern = re.compile(o['q']['parser'], re.IGNORECASE)
            re.sub(pattern, self.parse_query, self.uri['query'])
        
        return ParseUriDict(**self.uri) 
        
        