#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

try:
    from buildbot_pkg import setup_www_plugin
except ImportError:
    import sys
    print("Please install buildbot_pkg module in order to install that package, or use the pre-build .whl modules available on pypi", file=sys.stderr)
    sys.exit(1)


setup_www_plugin(
    name='buildbot-enhanced-ui-improved',
    description='A clearer and faster to manipulate interface for the management of BuildBot builders',
    author=u'Marc Leonardi',
    author_email=u'marc@goodbarber.com',
    version="1.0.1",
    license='',
    packages=['buildbot_enhanced_ui'],
    package_data={
        '': [
            'VERSION',
            'static/*'
        ]
    },
    entry_points="""
        [buildbot.www]
        buildbot_enhanced_ui = buildbot_enhanced_ui:ep
    """,
)
