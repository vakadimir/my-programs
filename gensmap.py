from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets

class WebEngineProfile(QtWebEngineWidgets.QWebEngineProfile):
    def __init__(self, parent=None):
        super(WebEngineProfile, self).__init__(parent)
        self.defaultProfile().setPersistentCookiesPolicy(QtWebEngineWidgets.QWebEngineProfile.NoPersistentCookies)
        self.defaultProfile().setHttpCacheType(QtWebEngineWidgets.QWebEngineProfile.NoCache)
        self.defaultProfile().setPersistentStoragePath('.')

        # Enable WebGL support
        settings = self.defaultProfile().settings()
        settings.setAttribute(QtWebEngineWidgets.QWebEngineSettings.WebGLEnabled, True)

class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self, profile, parent=None):
        super(WebEnginePage, self).__init__(profile, parent)

    def createWindow(self, _type):
        page = WebEnginePage(self.profile(), self)
        page.urlChanged.connect(self.on_url_changed)
        return page

    @QtCore.pyqtSlot(QtCore.QUrl)
    def on_url_changed(self, url):
        page = self.sender()
        self.setUrl(url)
        page.deleteLater()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Genshin Impact Interactive Map")
        profile = WebEngineProfile(self)
        self.browser = QtWebEngineWidgets.QWebEngineView()
        page = WebEnginePage(profile, self.browser)
        self.browser.setPage(page)
        self.browser.load(QtCore.QUrl("https://act.hoyolab.com/ys/app/interactive-map/index.html"))
        self.setCentralWidget(self.browser)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()
    sys.exit(app.exec_())
