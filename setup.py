# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '0.1'

README = open("README.rst").read()
HISTORY = open(os.path.join("docs", "HISTORY.rst")).read()

setup(name='base5.portlets',
      version=version,
      description="This product enables you to put portlets in places other than right and left columns",
      long_description=README + "\n" + HISTORY,
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='plone5, portlets',
      author='UPCnet Plone Team',
      author_email='plone.team@upcnet.es',
      url='https://github.com/UPCnet/base5.portlets',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['base5'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      extras_require={'test': ['plone.app.testing',
                               'plone.app.testing[robot]>=4.2.2',
                               'plone.app.robotframework[debug]',]},
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
