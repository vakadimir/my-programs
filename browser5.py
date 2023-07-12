import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class WebEngineView(QWebEngineView):
    def createWindow(self, window_type):
        if window_type == QWebEnginePage.WebBrowserTab:
            new_tab = browser.create_new_tab()
            new_tab.show()
            return new_tab.webview
        elif window_type == QWebEnginePage.WebBrowserBackgroundTab:
            new_tab = browser.create_new_tab()
            return new_tab.webview
        else:
            return super().createWindow(window_type)


class Browser(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1024, 768)
        self.url_bar = QLineEdit()
        self.back_button = QPushButton("←")
        self.forward_button = QPushButton("→")
        self.go_button = QPushButton("Go")
        self.new_tab_button = QPushButton("")
        self.webview = QWebEngineView()

        # Создание вкладок
        self.tabs = QTabWidget()
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        # Настройка виджетов
        self.back_button.setEnabled(True)
        self.forward_button.setEnabled(True)
        self.url_bar.returnPressed.connect(self.go_to_url)
        self.back_button.clicked.connect(self.webview.back)
        self.forward_button.clicked.connect(self.webview.forward)
        self.go_button.clicked.connect(self.go_to_url)
        self.new_tab_button.clicked.connect(self.create_new_tab)

        # Создание менеджеров компоновки и добавление виджетов в них
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.forward_button)
        button_layout.addWidget(self.go_button)
        button_layout.addWidget(self.url_bar)
        button_layout.setStretch(0, 1)
        button_layout.setSpacing(0)

        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.tabs)

        # Установка менеджера компоновки для окна
        self.setLayout(layout)

        # Создание первой вкладки и установка ее в качестве текущей
        self.create_new_tab()
        self.tabs.setCurrentIndex(0)

        # Размеры кнопок
        self.back_button.setFixedSize(25, 25)
        self.forward_button.setFixedSize(25, 25)
        self.go_button.setFixedSize(25, 25)
        self.new_tab_button.setFixedSize(0, 0)
        self.tabs.tabBarDoubleClicked.connect(self.create_new_tab)

    # Создание новой вкладки и функция ее закрытия
    def create_new_tab(self, url=None):
        new_tab = QWidget()
        layout = QVBoxLayout(new_tab)
        webview = WebEngineView(new_tab)
        layout.addWidget(webview)
        new_tab.setLayout(layout)
        self.tabs.addTab(new_tab, "Новая вкладка")
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(lambda index: self.tabs.removeTab(index))

        # Установка текущей вкладки
        index = self.tabs.count() - 1
        self.tabs.setCurrentIndex(index)

        # Настройка виджетов новой вкладки
        webview.loadStarted.connect(lambda: self.tabs.setTabText(index, "Loading..."))
        webview.loadFinished.connect(lambda: self.tabs.setTabText(index, webview.page().title()))

        webview.urlChanged.connect(lambda url: self.url_bar.setText(url.toString()))

        if url:
            webview.load(QUrl(url))
        else:
            webview.load(QUrl("https://www.google.com"))

        new_tab.webview = webview

        # Enable full-screen support for YouTube videos
        page = webview.page()
        page.fullScreenRequested.connect(self.enter_full_screen)

        return new_tab

    # Кнопка перехода или обновления
    def go_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url

        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.webview.load(QUrl(url))

    # Кнопки назад и вперед
    def backward(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.webview.page().triggerAction(QWebEnginePage.Back)

    def forward(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.webview.page().triggerAction(QWebEnginePage.Forward)

    # Вход в полноэкранный режим для YouTube видео
    def enter_full_screen(self, request):
        if request.toggleOn():

            self.tabs.tabBar().setVisible(False)
            self.url_bar.setVisible(False)
            self.back_button.setVisible(False)
            self.forward_button.setVisible(False)
            self.go_button.setVisible(False)

            self.showFullScreen()
            request.accept()
        else:

            self.tabs.tabBar().setVisible(True)
            self.url_bar.setVisible(True)
            self.back_button.setVisible(True)
            self.forward_button.setVisible(True)
            self.go_button.setVisible(True)

            self.showNormal()
            request.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('kvantum-dark')
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())
