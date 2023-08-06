from buildbot.www.plugin import Application


class BuildbotEnhancedUiApplication(Application):
    pass

# create the interface for the setuptools entry point
ep = BuildbotEnhancedUiApplication(__name__, "A clearer and faster to manipulate interface for the management of BuildBot builders")
