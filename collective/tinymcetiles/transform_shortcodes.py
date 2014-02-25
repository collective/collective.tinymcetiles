# -*- coding: utf-8 -*-
import urllib
from lxml.html import builder as E
from plone.transformchain.interfaces import ITransform
from plone.app.blocks import utils
from repoze.xmliter.serializer import XMLSerializer
from repoze.xmliter.serializer import lxml
from urlparse import urljoin
from zope.interface import implements

import logging
import re

logger = logging.getLogger('collective.tinymcetiles')

# if a shortcode contains this parameter it means that it represents
# a persistent tile
TILE_ID_PARAM = 'tile_id'

# use friendly names for shortcodes
# XXX: just a temp solution
SHORTCODE_TO_TILE_MAPPING = {
    'listing': 'plone.app.contentlistingtile'
}

# Regexp based on Wordpress' shortcode implementation
SHORTCODE_REGEXP = re.compile(
    r'\['  # Opening bracket
    r'(?P<escapeopen>\[?)'  # 1: Optional second opening bracket for escaping snippets: [[tag]]
    r'(?P<name>[/\w\d\_\.-@]+)'  # 2: Snippet name
    r'\b'  # Word boundary
    r'(?P<arguments>'  # 3: Unroll the loop: Inside the opening snippet tag
    r'[^\]\/]*'  # Not a closing bracket or forward slash
    r'(?:'
    r'\/(?!\])'  # A forward slash not followed by a closing bracket
    r'[^\]\/]*'  # Not a closing bracket or forward slash
    r')*?'
    r')'
    r'(?:'
    r'(?P<selfclosing>\/)'  # 4: Self closing tag ...
    r'\]'  # ... and closing bracket
    r'|'
    r'\]'  # Closing bracket
    r'(?:'
    r'(?P<content>'  # 5: Unroll the loop: Optionally, anything between the opening and closing snippet tags
    r'[^\[]*'  # Not an opening bracket
    r'(?:'
    r'\[(?!\/(?P=name)\])'  # An opening bracket not followed by the closing snippet tag
    r'[^\[]*'  # Not an opening bracket
    r')*'
    r')'
    r'\[\/(?P=name)\]'  # Closing snippet tag
    r')?'
    r')'
    r'(?P<escapeclose>\]?)')  # 6: Optional second closing bracket for escaping snippets: [[tag]]


class ShortcodesTransform(object):
    """Find shortcodes and replace them with tile output."""

    implements(ITransform)

    order = 8850

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def transformString(self, result, encoding):
        return self.transformIterable([result], encoding)

    def transformUnicode(self, result, encoding):
        return self.transformIterable([result], encoding)

    def transformIterable(self, result, encoding):
        if not self.request.get(
            'plone.app.blocks.enabled', False) or not isinstance(
                result, XMLSerializer):
            return None

        # go through all the potential shortcodes and try to resolve them
        # to tiles
        elements = result.tree.xpath("//*[contains(text(),'[')]")
        tree = result.tree
        for element in elements:
            #first see if we can find two matches at the same level
            shortcode_nodes = [element]
            for next in element.itersiblings():
                shortcode_nodes.append(next)
                if next in elements:
                    # shortcode_nodes now has '[' in start and end nodes
                    # due to how tinymce inserts things. our shortcode is likely something like
                    # <p>[code]</p><div/><p>[/code]</p>
                    text = shortcode_nodes[0].text
                    text += u''.join([lxml.html.tostring(n, encoding="ascii")
                                      for n in elements[1:-2]])
                    text += shortcode_nodes[-1].text
                    tile_tree, pre, post = self._get_tile_tree(text)
                    if tile_tree is None:
                        continue
                    tree = self._resolve_tile(tree, tile_tree, pre, post, shortcode_nodes)

        if tree is None:
            return None

        result.tree = tree

        # Set a marker in the request to let subsequent steps know the merging
        # has happened
        self.request['collective.tinymcetiles.merged'] = True

        return result

    def _resolve_tile(self, tree, tile_tree, pre, post, elements=[]):
        """Try to resolve the tile and merge it into the tree."""

        root = tree.getroot()
        self._merge_head(root, tile_tree)

        # replace the element's text with the tile body
        # XXX: this should be done differently probably
        tileBody = tile_tree.find('body')
        if tileBody is None:
            return tree

        # insert nodes before out matched nodes
        # insert tile target with tile body
        # Preserve text
        first = elements[0]
        if pre:
            n = E.SPAN()
            n.text = pre
            first.addprevious(n)
        if tileBody.text:
            tileTextSpan = E.SPAN()
            tileTextSpan.text = tileBody.text
            first.addprevious(tileTextSpan)

        # Copy other nodes
        for tileBodyChild in tileBody:
            first.addprevious(tileBodyChild)
        if post:
            n = E.SPAN()
            n.text = post
            first.addprevious(n)

        # remove the matched nodes
        parent = first.getparent()
        for child in elements:
            parent.remove(child)
        return tree

    def _merge_head(self, root, tile_tree):
        head_node = root.find('head')

        # merge tile head into the page's head
        tile_head = tile_tree.find('head')
        if tile_head is not None:
            for node in tile_head:
                head_node.append(node)

    def _get_tile_tree(self, text):
        """Find shortcodes in the provided text and resolve them to tiles.

        Note: code borrowed from pyramid_snippets
        """

        def parse_text(text):
            match = SHORTCODE_REGEXP.search(text)
            if not match:
                return (None, None)
            pre = text[:match.start()]
            post = text[match.end():]

            infos = match.groupdict()
            if infos['selfclosing'] is None and infos['content'] is None:
                return (None, None, pre, post)
            if infos['escapeopen'] and infos['escapeclose']:
                return ''.join((
                    infos['escapeopen'],
                    infos['name'],
                    infos['arguments'],
                    infos['selfclosing'],
                    infos['escapeclose']))
            arguments = {}
            last_key = None
            for arg in infos['arguments'].split(' '):
                if '=' in arg:
                    key, value = arg.split('=')
                    key = key.strip()
                    value = value.strip().strip('"')
                    arguments[key] = value
                    last_key = key
                elif last_key is not None:
                    arguments[last_key] = '%s %s' % (arguments[last_key], arg)
            arguments['body'] = infos['content']

            return (infos['name'], arguments, pre, post)

        name, arguments, pre, post = parse_text(text)
        return self._get_tile(name=name, arguments=arguments), pre, post

    def _get_tile(self, name=None, arguments=None):
        """Get the tile for the specified shortcode arguments.

        :param name: friendly name of the tile, which maps to the actual
                     tile id
        :param arguments: arguments for tile creation
        """
        if name is None or arguments is None:
            return

        if name in SHORTCODE_TO_TILE_MAPPING:
            name = SHORTCODE_TO_TILE_MAPPING[name]
        baseURL = self.request.getURL()
        if name[0] not in ['.', '@', '/']:
            tileHref = urljoin(baseURL, '@@' + name)
        else:
            tileHref = urljoin(baseURL, name)

        # persistent tile
        if TILE_ID_PARAM in arguments:
            tileId = arguments[TILE_ID_PARAM].strip()
            tileHref = '{0}/{1}'.format(tileHref, tileId)

        # create a new transient tile
        #context = self.published.aq_parent
        #HACK: we need to encode it into the url again
        #self.request.form.update(arguments)
        #tile = getMultiAdapter((context, self.request), name=name)
        if arguments:
            tileHref += '?' + urllib.urlencode(arguments)

        return utils.resolve(tileHref)
