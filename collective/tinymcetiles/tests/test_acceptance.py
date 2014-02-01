# -*- coding: utf-8 -*-
import unittest
import robotsuite
from plone.testing import layered
from collective.tinymcetiles.testing import TILES_ROBOT_TESTING
import urllib
import os


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('test_acceptance.robot'),
                layer=TILES_ROBOT_TESTING),
    ])
    return suite


class Keywords(object):
    """Robot Framework keyword library"""

    def download_file(self, url):
        filename, headers = urllib.urlretrieve(url)
        statinfo = os.stat(filename)
        if statinfo.st_size == 0:
            raise Exception("file download failed")
        return filename
