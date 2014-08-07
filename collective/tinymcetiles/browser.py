# -*- coding: utf-8 -*-
from plone.app.tiles.browser.add import DefaultAddForm
from plone.app.tiles.browser.add import DefaultAddView
from plone.app.tiles.browser.edit import DefaultEditForm
from plone.app.tiles.browser.edit import DefaultEditView
from plone.app.tiles.utils import appendJSONData
from plone.app.tiles.utils import getEditTileURL
from zope.traversing.browser.absoluteurl import absoluteURL


class TinyMCETilesAddForm(DefaultAddForm):

    def nextURL(self, tile):
        # Calculate the edit URL and append some data in a JSON structure, to
        # help the UI know what to do.

        tileTypeName = self.tileType.__name__
        tileURL = absoluteURL(tile, self.request)

        contextURL = absoluteURL(tile.context, self.request)
        tileRelativeURL = tileURL
        if tileURL.startswith(contextURL):
            tileRelativeURL = '.' + tileURL[len(contextURL):]

        tileEditURL = getEditTileURL(tile, self.request)
        tileDataJSON = {}
        tileDataJSON['action'] = "save"
        tileDataJSON['mode'] = "add"
        tileDataJSON['url'] = tileRelativeURL
        tileDataJSON['tile_type'] = tileTypeName
        tileDataJSON['id'] = tile.id

        url = appendJSONData(tileEditURL, 'tiledata', tileDataJSON)
        return url


class TinyMCETilesAddView(DefaultAddView):
    form = TinyMCETilesAddForm


class TinyMCETilesEditForm(DefaultEditForm):

    def nextURL(self, tile):
        # Calculate the edit URL and append some data in a JSON structure, to
        # help the UI know what to do.

        tileTypeName = self.tileType.__name__
        tileURL = absoluteURL(tile, self.request)

        contextURL = absoluteURL(tile.context, self.request)
        tileRelativeURL = tileURL
        if tileURL.startswith(contextURL):
            tileRelativeURL = '.' + tileURL[len(contextURL):]

        tileEditURL = getEditTileURL(tile, self.request)
        tileDataJSON = {}
        tileDataJSON['action'] = "save"
        tileDataJSON['mode'] = "edit"
        tileDataJSON['url'] = tileRelativeURL
        tileDataJSON['tile_type'] = tileTypeName
        tileDataJSON['id'] = tile.id

        url = appendJSONData(tileEditURL, 'tiledata', tileDataJSON)
        return url


class TinyMCETilesEditView(DefaultEditView):
    form = TinyMCETilesEditForm
