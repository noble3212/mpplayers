import sys
import vlc
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QLabel, QGroupBox, QMessageBox
)
from PyQt5.QtCore import Qt

class MP4Player(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MP4 Player (VLC Backend)")
        self.setGeometry(100, 100, 800, 600)

        self.instance = vlc.Instance()
        self.mediaPlayer = self.instance.media_player_new()

        # Title label
        title = QLabel("🎬 MP4 Player")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")

        # File label
        self.file_label = QLabel("No file loaded")
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setStyleSheet("color: gray; margin-bottom: 10px;")

        # Control buttons
        openBtn = QPushButton('Open MP4')
        openBtn.clicked.connect(self.open_file)
        playBtn = QPushButton('Play')
        playBtn.clicked.connect(self.play_video)
        pauseBtn = QPushButton('Pause')
        pauseBtn.clicked.connect(self.mediaPlayer.pause)
        stopBtn = QPushButton('Stop')
        stopBtn.clicked.connect(self.mediaPlayer.stop)

        # Arrange controls horizontally
        controls = QHBoxLayout()
        controls.addWidget(openBtn)
        controls.addWidget(playBtn)
        controls.addWidget(pauseBtn)
        controls.addWidget(stopBtn)

        controls_group = QGroupBox("Controls")
        controls_group.setLayout(controls)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.file_label)
        layout.addWidget(controls_group)
        layout.addStretch()

        self.setLayout(layout)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open MP4 File", "", "MP4 Files (*.mp4)")
        if filename != '':
            self.file_label.setText(f"Loaded: {filename}")
            media = self.instance.media_new(filename)
            self.mediaPlayer.set_media(media)
            # Set the video output window
            if sys.platform.startswith('linux'):
                self.mediaPlayer.set_xwindow(self.winId())
            elif sys.platform == "win32":
                self.mediaPlayer.set_hwnd(int(self.winId()))
            elif sys.platform == "darwin":
                self.mediaPlayer.set_nsobject(int(self.winId()))
        else:
            self.file_label.setText("No file loaded")

    def play_video(self):
        if self.mediaPlayer.get_media() is None:
            QMessageBox.warning(self, "No File", "Please open an MP4 file first.")
            return
        self.mediaPlayer.play()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            # Stop video and reset to menu state
            self.mediaPlayer.stop()
            self.file_label.setText("No file loaded\nPress 'Open MP4' to select a file.")
        else:
            super().keyPressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MP4Player()
    player.show()
    sys.exit(app.exec_())
