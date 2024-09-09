import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QFileDialog, QSlider, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


#My app
class AudioApp(QWidget) :
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.event_handler()
    
    # Settings

    def settings(self):
        self.setWindowTitle("Aud-Just")
        self.setGeometry(500, 500, 600, 300)
        # self.resize(600, 300) Alternative to setgeometry
    # Design

    def initUI(self):
        self.title = QLabel('Audio Adjuster')
        self.title.setObjectName('title')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.file_list = QListWidget()
        self.btn_opener = QPushButton("Choose a File")
        self.btn_play = QPushButton("Play")
        self.btn_pause  = QPushButton("Pause")
        self.btn_resume  = QPushButton("Resume")
        self.btn_reset  = QPushButton("Reset")

        #Decative buttons initially
        self.btn_pause.setDisabled(True)
        self.btn_resume.setDisabled(True)
        self.btn_reset.setDisabled(True)

        self.slider =QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(50)
        self.slider.setMaximum(150)
        self.slider.setValue(100)
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.slider_text = QLabel("Speed: 100x")
        self.slider_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.slider_text)
        slider_layout.addWidget(self.slider)
    
    # Create layout
        self.master= QVBoxLayout()
        row =QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        self.master.addWidget(self.title)
        self.master.addLayout(slider_layout)

        col1.addWidget(self.file_list)
        col2.addWidget(self.btn_opener)
        col2.addWidget(self.btn_play)
        col2.addWidget(self.btn_pause)
        col2.addWidget(self.btn_resume)
        col2.addWidget(self.btn_reset)

        row.addLayout(col1)
        row.addLayout(col2)
        self.style()
        self.master.addLayout(row)
        self.setLayout(self.master)

        # Special audio classes from pyQt
        self.audio_output = QAudioOutput()
        self.media_player = QMediaPlayer()
        self.media_player.setAudioOutput(self.audio_output)
    
    # Styling
    def style(self):
        self.setStyleSheet("""
                            Qwidget {
                        background-Color: #F98BBA ;
                        }
                        
                        QPushButton {
                        background-Color: #5BB9C2 ;
                        padding: 15px;
                        border-radius: 10px;
                        color: #333;
                        }
                        
                        QPushButton:hover {
                        background-Color: #1A4870 ;
                        color: #F98BBA;
                        }
                        
                        QLabel {
                        color: #333
                        }

                        #title {
                        font-family: Papyrus;
                        font-size: 40px;
                        }

                        QSlider {
                        margin-right: 15px;
                        }

                        QListWidget {
                        color: #333;
                        }
                        """)

    # Event Handler
    def event_handler(self):
        self.slider.valueChanged.connect(self.update_slider)
        self.btn_opener.clicked.connect(self.open_file)
        self.btn_play.clicked.connect(self.play_audio)
        self.btn_pause.clicked.connect(self.pause_audio)
        self.btn_resume.clicked.connect(self.resume_audio)
        self.btn_reset.clicked.connect(self.reset_audio)


    # Change slider speed label
    def update_slider(self):
        speed =self.slider.value()/100
        self.slider_text.setText(f"Speed: {speed:.2f}x")

    # Working with the directory

    def open_file(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")

        if path:
            self.file_list.clear()
            for file_name in os.listdir(path):
                if file_name.endswith(".mp3"):
                    self.file_list.addItem(file_name)
        
        else :
            file, _ =QFileDialog.getOpenFileName(self, "Select File", filter = "Audio Files(*.mp3)")
            if file:
                self.file_list.clear()
                self.file_list.addItem(os.path.basename(file))
    
    # Play the audio file
    def play_audio(self):
        if self.file_list.selectedItems():
            file_name = self.file_list.selectedItems()[0].text()
            folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
            file_path = os.path.join(folder_path,file_name)
            file_url = QUrl.fromLocalFile(file_path)

            self.media_player.setSource(file_url)
            self.media_player.setPlaybackRate(self.slider.value()/100.0)
            self.media_player.play()
            self.btn_pause.setEnabled(True)
            self.btn_resume.setDisabled(True)
            self.btn_reset.setEnabled(True)
            self.btn_play.setDisabled(True)

    def pause_audio(self):
        self.media_player.pause()
        self.btn_pause.setDisabled(True)
        self.btn_resume.setEnabled(True)
    
    def resume_audio(self):
        self.media_player.play()
        self.btn_pause.setEnabled(True)
        self.btn_resume.setDisabled(True)
    
    def reset_audio(self):
        if self.media_player.isPlaying():
            self.media_player.stop()
        
        self.media_player.setPosition(0)
        self.media_player.setPlaybackRate(self.slider.value()/100.0)
        self.media_player.play()

        self.btn_pause.setEnabled(True)
        self.btn_resume.setDisabled(True)
        self.btn_reset.setEnabled(True)
        self.btn_play.setDisabled(True)

        QTimer.singleShot(100, lambda: self.btn_reset.setEnabled)
    
#Boilerplate

if __name__ in "__main__":
    app = QApplication([])
    main =AudioApp()
    main.show()
    app.exec()


