from winreg import HKEY_CURRENT_USER
import utils.registry

try:
    SYSTEM_THEME = utils.registry.read_key(HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize", "AppsUseLightTheme")

    if SYSTEM_THEME:
        SYSTEM_THEME = "LIGHT" 
    
    else:
        SYSTEM_THEME = "DARK"

except FileNotFoundError:
    SYSTEM_THEME = "LIGHT"

class Styles:
    if SYSTEM_THEME == "LIGHT":
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

                        QWidget#footer QPushButton#main_buttons {
                            padding: 5px;
                            padding-left: 15px;
                            padding-right: 15px;
                            background-color: rgb(230, 230, 230);
                            border: 1px solid rgb(64, 64, 64);
                            color: rgb(64, 64, 64);
                        }

                        QWidget#footer QPushButton#main_buttons:hover {
                            background-color: rgb(230, 230, 230);
                            border: 1px solid rgb(96, 96, 96);
                            color: rgb(96, 96, 96);
                        }

                        QWidget#footer QPushButton#main_buttons:pressed {
                            background-color:rgb(205, 205, 205);
                            border: 1px solid rgb(128, 128, 128);
                            color: rgb(128, 128, 128);
                        }

                        QWidget#footer QPushButton#main_buttons:disabled {
                            background-color: rgb(205, 205, 205);
                            border: 1px solid rgb(96, 96, 96);
                            color: rgb(96, 96, 96);
                        }

                        QWidget#footer QPushButton#support_me_button {
                            background-color: rgb(225, 225, 225);
                            border: 1px solid rgb(192, 192, 192);
                            color: rgb(0, 0, 0);
                            padding: 2px;
                            border-radius: 2px;
                        }

                        QWidget#footer QPushButton#support_me_button:hover {
                            background-color: rgb(225, 225, 225);
                            border: 1px solid rgb(214, 214, 214);
                            color: rgb(22, 22, 22);
                            text-decoration: underline;
                        }

                        QWidget#footer QPushButton#support_me_button:pressed {
                            background-color: rgb(225, 225, 225);
                            color: rgb(65, 65, 65);
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

                                QWidget#settings QPushButton#support_me_button {
                                    background-color: rgb(225, 225, 225);
                                    border: 1px solid rgb(192, 192, 192);
                                    color: rgb(0, 0, 0);
                                    padding: 2px;
                                    border-radius: 2px;
                                }

                                QWidget#settings QPushButton#support_me_button:hover {
                                    background-color: rgb(225, 225, 225);
                                    border: 1px solid rgb(214, 214, 214);
                                    color: rgb(22, 22, 22);
                                    text-decoration: underline;
                                }

                                QWidget#settings QPushButton#support_me_button:pressed {
                                    background-color: rgb(225, 225, 225);
                                    color: rgb(65, 65, 65);
                                }
                                """

        MessageBoxStyle = """
        
                        """
    
    elif SYSTEM_THEME == "DARK":
        MainWindowStyle = """
                        QWidget#main {
                            background-color: #1e1e1e;
                        }


                        QLabel#textbox_title{
                            padding: 2px;
                            color: rgb(191, 191, 191);
                        }

                        QLabel#textbox_box{
                            background-color: black;
                            color: rgb(191, 191, 191);
                            padding: 5px;
                            border-radius: 3px;
                        }

                        QWidget#footer {
                            border-top: 1px solid #3f3f3f;
                            background-color: #000f0a;
                        }

                        QWidget#footer QLabel{
                            color: rgb(191, 191, 191);
                        }

                        QWidget#footer QPushButton#main_buttons {
                            padding: 5px;
                            padding-left: 15px;
                            padding-right: 15px;
                            background-color: rgb(25, 25, 25);
                            border: 1px solid rgb(191, 191, 191);
                            color: rgb(191, 191, 191);
                        }

                        QWidget#footer QPushButton#main_buttons:hover {
                            background-color: rgb(25, 25, 25);
                            border: 1px solid rgb(159, 159, 159);
                            color: rgb(159, 159, 159);
                        }

                        QWidget#footer QPushButton#main_buttons:pressed {
                            background-color:rgb(40, 40, 40);
                            border: 1px solid rgb(128, 128, 128);
                            color: rgb(128, 128, 128);
                        }

                        QWidget#footer QPushButton#main_buttons:disabled {
                            background-color: rgb(40, 40, 40);
                            border: 1px solid rgb(159, 159, 159);
                            color: rgb(159, 159, 159);
                        }

                        QWidget#footer QPushButton#support_me_button {
                            background-color: rgb(30, 30, 30);
                            border: 1px solid rgb(63, 63, 63);
                            color: rgb(191, 191, 191);
                            padding: 2px;
                            border-radius: 2px;
                        }

                        QWidget#footer QPushButton#support_me_button:hover {
                            background-color: rgb(30, 30, 30);
                            border: 1px solid rgb(41, 41, 41);
                            color: rgb(159,159,159);
                            text-decoration: underline;
                        }

                        QWidget#footer QPushButton#support_me_button:pressed {
                            background-color: rgb(30, 30, 30);
                            color: rgb(128, 128, 128);
                        }
                        
                        """

        SettingsWindowStyle = """
                                QWidget#settings {
                                background-color: #1e1e1e;
                                color: rgb(191, 191, 191);
                                }

                                QWidget#settings QWidget#option_box {
                                    border: 1px solid #3f3f3f;
                                    background-color: #000f0a;
                                    padding: 5px;
                                }

                                QWidget#settings QWidget#option_box QLabel{
                                    color: rgb(191, 191, 191);
                                }

                                QWidget#settings QWidget#option_box QCheckBox{
                                    color: rgb(191, 191, 191);
                                }

                                QWidget#settings QPushButton#support_me_button {
                                    background-color: rgb(0, 15, 10);
                                    border: 1px solid rgb(63, 63, 63);
                                    color: rgb(191, 191, 191);
                                    padding: 2px;
                                    border-radius: 2px;
                                }

                                QWidget#settings QPushButton#support_me_button:hover {
                                    background-color: rgb(0, 15, 10);
                                    border: 1px solid rgb(41, 41, 41);
                                    color: rgb(159,159,159);
                                    text-decoration: underline;
                                }

                                QWidget#settings QPushButton#support_me_button:pressed {
                                    background-color: rgb(0, 15, 10);
                                    color: rgb(128, 128, 128);
                                }
                                """
        
        MessageBoxStyle = """
                            QMessageBox#msgbox {
                                background-color: #1e1e1e;
                            }

                            QMessageBox#msgbox QPushButton {
                            padding: 5px;
                            padding-left: 15px;
                            padding-right: 15px;
                            background-color: rgb(25, 25, 25);
                            border: 1px solid rgb(191, 191, 191);
                            color: rgb(191, 191, 191);
                            }

                            QMessageBox#msgbox QPushButton:hover {
                                background-color: rgb(25, 25, 25);
                                border: 1px solid rgb(159, 159, 159);
                                color: rgb(159, 159, 159);
                            }

                            QMessageBox#msgbox QPushButton:pressed {
                                background-color:rgb(40, 40, 40);
                                border: 1px solid rgb(128, 128, 128);
                                color: rgb(128, 128, 128);
                            }

                            QMessageBox#msgbox QLabel {
                                color: white;
                            }
                        """
    
