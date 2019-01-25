#coding=utf-8
'''
Created on 2016-9-29

@author: zhangtiande
'''

import json
from collections import OrderedDict
from django.utils import six
from rest_framework.renderers import JSONRenderer
from rest_framework.compat import (
    INDENT_SEPARATORS, LONG_SEPARATORS, SHORT_SEPARATORS
)

class TeamvisionJSONRenderer(JSONRenderer):
    
    
    def __init__(self):
        JSONRenderer.__init__(TeamvisionJSONRenderer)
        self.code=1
        self.message="test"
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return bytes()

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS
            
        new_data=OrderedDict()
        new_data['code']=renderer_context['response'].status_code
        new_data['message']=renderer_context['response'].status_text
        new_data['result']=data
        ret = json.dumps(
            new_data, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii,
            separators=separators
        )

        # On python 2.x json.dumps() returns bytestrings if ensure_ascii=True,
        # but if ensure_ascii=False, the return type is underspecified,
        # and may (or may not) be unicode.
        # On python 3.x json.dumps() returns unicode strings.
        if isinstance(ret, six.text_type):
            # We always fully escape \u2028 and \u2029 to ensure we output JSON
            # that is a strict javascript subset. If bytes were returned
            # by json.dumps() then we don't have these characters in any case.
            # See: http://timelessrepo.com/json-isnt-a-javascript-subset
            ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
            return bytes(ret.encode('utf-8'))
        return ret
