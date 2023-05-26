from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from PyQt5 import QtGui
from yt_dlp import YoutubeDL
import os

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)  # Load the UI file

        self.URLs = []  # Create a list to store the URLs
        self.DlURLs = []  # Create a list to store the URLs
        self.AddButton.clicked.connect(self.addUrl)  # Connect the button to a function
        self.RemoveButton.clicked.connect(self.removeUrl)  # Connect the button to a function
        self.DownloadButton.clicked.connect(self.download_videos)  # Connect the button to a function

        self.setWindowTitle("YTDL")  # Set the window title
        self.setWindowIcon(QtGui.QIcon('icon.ico'))

        # Connect radio button toggled signals to update format
        self.Mp3Button.toggled.connect(lambda: self.update_format("mp3"))
        self.Mp41080Button.toggled.connect(lambda: self.update_format("mp4"))

        # Connect the PathButton's clicked signal to the open_folder_dialog function
        self.PathButton.clicked.connect(self.open_folder_dialog)

        # Initialize the format option
        self.format_option = "mp3"  # Default format
        self.path = os.getcwd()  # Default path
        self.PathInput.setText(self.path)  # Set the path input box to the default path

        self.set_status("Ready")

    def addUrl(self):
        url = self.UrlInput.text()  # Get the text in the input box
        if url == "":
            return
        self.UrlList.addItem(url)  # Add the text to the list
        print(f"Added URL: {url}")  # Print the text in the input box
        self.URLs.append(url)  # Add the text to the list
        self.set_status("List Item Added")

    def removeUrl(self):
        url = self.UrlList.currentItem()  # Get the text of the selected item
        if url is not None:
            self.UrlList.takeItem(self.UrlList.row(url))  # Remove the item from the list
            self.URLs.remove(url.text())  # Remove the item from the list
            self.set_status("List Item Removed")

    def open_folder_dialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        
        if dialog.exec_() == QFileDialog.Accepted:
            folder_path = dialog.selectedFiles()[0]
            self.path = folder_path
            self.PathInput.setText(self.path)
            self.set_status(f"Output Path Changed: {self.path}")

    def update_format(self, format_option):
        self.format_option = format_option
        self.set_status(f"Format Changed to {format_option}")

    def download_videos(self):
        ydl_opts = {
            'format': self.get_format_option(),
            'outtmpl': os.path.join(self.path, '%(title)s.%(ext)s')
        }  # Additional options for youtube-dl can be specified here

        with YoutubeDL(ydl_opts) as ydl:
            for url in self.URLs:
                ydl.download([url])
                self.DlURLs.append(url)

        self.set_status("Success!")

    def get_format_option(self):
        if self.format_option == "mp3":
            return "bestaudio/best"
        elif self.format_option == "mp4":
            return 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'

        return "best"

    def set_status(self, status):
        self.DownloadOutput.setText(status)

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
