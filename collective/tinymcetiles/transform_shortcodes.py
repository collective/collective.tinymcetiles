from urlparse import urljoin
from plone.transformchain.interfaces import ITransform
from plone.app.blocks import utils
from repoze.xmliter.serializer import XMLSerializer
from zope.interface import implements

import logging
import re

logger = logging.getLogger('collective.tinymcetiles')

# use friendly names for shortcodes
# XXX: just a temp solution
SHORTCODE_TO_TILE_MAPPING = {
    'listing': 'plone.app.contentlistingtile'
}

# Regexp based on Wordpress' shortcode implementation
SHORTCODE_REGEXP = re.compile(
    r'\['  # Opening bracket
    r'(?P<escapeopen>\[?)'  # 1: Optional second opening bracket for escaping snippets: [[tag]]
    r'(?P<name>[/\w\d\_\.-]+)'  # 2: Snippet name
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
            tree = self._resolve_tile(tree, element)

        if tree is None:
            return None

        result.tree = tree

        # Set a marker in the request to let subsequent steps know the merging
        # has happened
        self.request['collective.tinymcetiles.merged'] = True

        return result

    def _resolve_tile(self, tree=None, element=None):
        """Try to resolve the tile and merge it into the tree."""

        root = tree.getroot()
        head_node = root.find('head')
        tile_tree = self._get_tile_tree(element.text)

        if tile_tree is None:
            return tree

        # merge tile head into the page's head
        tile_head = tile_tree.find('head')
        if tile_head is not None:
            for node in tile_head:
                head_node.append(node)

        # replace the element's text with the tile body
        # XXX: this should be done differently probably
        tile_body = tile_tree.find('body')
        if tile_body is not None:
            element.text = tile_body.text
        return tree

    def _get_tile_tree(self, text):
        """Find shortcodes in the provided text and resolve them to tiles.

        Note: code borrowed from pyramid_snippets
        """

        def parse_text(text):
            match = SHORTCODE_REGEXP.match(text)
            if not match:
                return (None, None)
            infos = match.groupdict()
            if infos['selfclosing'] is None and infos['content'] is None:
                return (None, None)
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
                    value = value.strip()
                    arguments[key] = value
                    last_key = key
                elif last_key is not None:
                    arguments[last_key] = "%s %s" % (arguments[last_key], arg)
            arguments['body'] = infos['content']

            return (infos['name'], arguments)

        name, arguments = parse_text(text)
        return self._create_tile(name=name, params=arguments)

    def _create_tile(self, name=None, params=None):
        """Create a transient tile."""
        if name in SHORTCODE_TO_TILE_MAPPING:
            name = SHORTCODE_TO_TILE_MAPPING.get(name, None)
        baseURL = self.request.getURL()
        tileHref = urljoin(baseURL, '@@' + name)

        # create a new transient tile
        #context = self.published.aq_parent
        #HACK: we need to encode it into the url again
        self.request.form.update(params)
        #tile = getMultiAdapter((context, self.request), name=name)

        return utils.resolve(tileHref)
