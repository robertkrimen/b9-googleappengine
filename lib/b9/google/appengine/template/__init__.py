# http://appengine-cookbook.appspot.com/recipe/using-custom-django-template-helpers/?id=ahJhcHBlbmdpbmUtY29va2Jvb2tyjgELEgtSZWNpcGVJbmRleCI4YWhKaGNIQmxibWRwYm1VdFkyOXZhMkp2YjJ0eUZBc1NDRU5oZEdWbmIzSjVJZ1pFYW1GdVoyOE0MCxIGUmVjaXBlIjlhaEpoY0hCbGJtZHBibVV0WTI5dmEySnZiMnR5RkFzU0NFTmhkR1ZuYjNKNUlnWkVhbUZ1WjI4TTAM

from google.appengine.ext import webapp
from django import template
import logging;

register = webapp.template.create_template_register()

def truncate(value, length = 24):
    if len(value) < length:
        return value
    else:
        return value[:length] + '...'

register.filter(truncate)

#webapp.template.register_template_library('common.templatefilters')

binaryTest_map = {
    'lt': lambda x,y: x < y,
    'lte': lambda x,y: x <= y,
    'gt': lambda x,y: x > y,
    'gte': lambda x,y: x >= y,
    'eq': lambda x,y: x == y,
    'ne': lambda x,y: x != y,
    'in': lambda x,y: x in y,
    'not_in': lambda x,y: x not in y,
}

unaryTest_map = {
    'empty': lambda x: x is None or len(x) == 0,
    'not_empty': lambda x: x is not None and len(x) != 0,
#    'not_empty': lambda x: x is not None and len(x) != 0,
#    'not_empty': lambda x: x is not None and x != "" and len(x) != 0,
}

class BinaryNode(template.Node):
    def __init__(self, a, b, comparison, nodelist_true, nodelist_false):
        self.a = a
        self.b = b
        self.comparison = comparison
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
    
    def render(self, context):
        try:
            a = template.resolve_variable(self.a, context)
            b = template.resolve_variable(self.b, context)
            if binaryTest_map[self.comparison](a, b):
                return self.nodelist_true.render(context)
        except template.VariableDoesNotExist:
            return ''
        except TypeError:
            return ''
        return self.nodelist_false.render(context)

def binaryTest(parser, token):
    token_part = token.contents.split()
    if len(token_part) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % token_part[0])
    nodelist_true = parser.parse(('else', 'end', 'end' + token_part[0]))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('end', 'end' + token_part[0]))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    comparison = token_part[0].split('if_')[1]
    return BinaryNode(token_part[1], token_part[2], comparison, nodelist_true, nodelist_false)

class UnaryNode(template.Node):
    def __init__(self, a, comparison, nodelist_true, nodelist_false):
        self.a = a
        self.comparison = comparison
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
    
    def render(self, context):
        try:
            a = template.resolve_variable(self.a, context)
            if unaryTest_map[self.comparison](a):
                return self.nodelist_true.render(context)
        except template.VariableDoesNotExist:
            return ''
        except TypeError:
            return ''
        return self.nodelist_false.render(context)

def unaryTest(parser, token):
    token_part = token.contents.split()
    if len(token_part) != 2:
        raise template.TemplateSyntaxError("'%s' tag takes one argument" % token_part[0])
    nodelist_true = parser.parse(('else', 'end', 'end' + token_part[0]))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('end', 'end' + token_part[0]))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()
    comparison = token_part[0].split('if_')[1]
    return UnaryNode(token_part[1], comparison, nodelist_true, nodelist_false)

for tag_name in (
    'if_lt', 'if_lte', 'if_gt', 'if_gte', 'if_eq', 'if_ne',
    'if_in', 'if_not_in',
    ):
    register.tag(tag_name, binaryTest)

for tag_name in (
    'if_empty', 'if_not_empty',
    ):
    register.tag(tag_name, unaryTest)
