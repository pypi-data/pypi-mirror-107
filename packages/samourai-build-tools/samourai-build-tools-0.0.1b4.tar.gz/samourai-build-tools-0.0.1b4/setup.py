#!/usr/bin/env python

from setuptools import setup

setup(name='samourai-build-tools',
      use_scm_version=True,
      setup_requires=["setuptools_scm"],
      description='CircuitPython library build tools',
      author='Scott Shawcroft',
      author_email='scott@adafruit.com',
      url='https://www.adafruit.com/',
      packages=['samourai_build_tools',
                'samourai_build_tools.scripts'],
      zip_safe=False,
      python_requires='>=3.7',
      install_requires=['Click', 'requests', 'semver'],
      entry_points='''
        [console_scripts]
        circuitpython-build-bundles=samourai_build_tools.scripts.build_bundles:build_bundles
      '''
      )
