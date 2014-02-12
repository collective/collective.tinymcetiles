from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='collective.tinymcetiles',
      version=version,
      description="TinyMCE Plugin for Tiles",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Rob Gietema',
      author_email='rob@fourdigits.nl',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
<<<<<<< HEAD
          'setuptools',
          'plone.api',
          'plone.app.tiles',
=======
>>>>>>> master
          'plone.app.blocks',
          'plone.app.tiles',
          'Products.GenericSetup',
          'Products.TinyMCE',
          'setuptools',
          'zope.interface',
      ],
      extras_require={
          'test': [
              'plone.app.contentlistingtile',
              'plone.app.contenttypes',
              'plone.app.event',
              'plone.app.robotframework >=0.7.0rc4',
              'plone.app.testing',
              'plone.app.texttile',
              'plone.registry',
              'plone.testing',
              'robotframework-selenium2screenshots',
              'collective.js.speakjs',
              'robotsuite',
              'transaction',
              'unittest2',
              'zope.component',
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
