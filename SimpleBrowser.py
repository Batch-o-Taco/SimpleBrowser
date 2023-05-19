import os
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLineEdit, QMainWindow, QPushButton, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile

EDGE_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"

class Tab(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.load(QUrl("https://www.bing.com"))

        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent(EDGE_USER_AGENT)
        profile.downloadRequested.connect(self.on_download_requested)

    def on_download_requested(self, download):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getSaveFileName(self, "Guardar como", download.suggestedFileName(), options=options)
        if path:
            download.setPath(path)
            download.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.layout.addWidget(self.tabs)

        self.add_tab_button = QPushButton("+")
        self.add_tab_button.clicked.connect(self.add_tab)
        self.tabs.setCornerWidget(self.add_tab_button)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.layout.addWidget(self.url_bar)

        self.add_tab()

    def add_tab(self):
        new_tab = Tab()
        i = self.tabs.addTab(new_tab, "Nueva Pestaña")
        self.tabs.setCurrentIndex(i)

    def close_tab(self, index):
        if index != 0:
            tab = self.tabs.widget(index)
            tab.deleteLater()
            self.tabs.removeTab(index)

    def navigate_to_url(self):
        url_text = self.url_bar.text()
        if not url_text.startswith("https://") and not url_text.startswith("http://"):
            url_text = "https://" + url_text
        url = QUrl(url_text)
        current_tab = self.tabs.currentWidget()
        current_tab.load(url)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
