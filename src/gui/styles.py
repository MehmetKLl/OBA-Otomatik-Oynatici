class Styles:
    MainWindowStyle = """
                    QWidget#main {
                        background-color: #e1e1e1;
                    }


                    QLabel#textbox_title{
                        padding: 2px;
                    }

                    QLabel#textbox_box{
                        background-color: white;
                        padding: 5px;
                        border-radius: 3px;
                    }

                    QWidget#footer {
                        border-top: 1px solid #c0c0c0;
                        background-color: #fff0f5;
                    }

                    QWidget#footer QPushButton {
                        padding: 5px;
                        padding-left: 15px;
                        padding-right: 15px;
                        background-color: rgb(230,230,230);
                        border: 1px solid rgb(64,64,64);
                        color: rgb(64,64,64);
                    }

                    QWidget#footer QPushButton:hover {
                        background-color: rgb(230,230,230);
                        border: 1px solid rgb(96,96,96);
                        color: rgb(96,96,96);
                    }

                    QWidget#footer QPushButton:pressed {
                        background-color:rgb(205,205,205);
                        border: 1px solid rgb(128,128,128);
                        color: rgb(128,128,128);
                    }

                    QWidget#footer QPushButton:disabled {
                        background-color: rgb(205,205,205);
                        border: 1px solid rgb(96,96,96);
                        color: rgb(96,96,96);
                    }
                    
                    """

    SettingsWindowStyle = """
                            QWidget#settings {
                            background-color: #e1e1e1;
                            }

                            QWidget#settings QWidget#option_box {
                            border: 1px solid #c0c0c0;
                            background-color: #fff0f5;
                            padding: 5px;
                            }
                            """