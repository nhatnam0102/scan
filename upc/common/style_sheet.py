main_color = "#458b74"
main_color_rgb = (69, 139, 116)
bg_color = "white"  # "Gainsboro"
btn_bg_color = "white"
btn_bg_press_color = "Gainsboro"
btn_bg_hover_color = "white"
btn_text_color = "black"
bor_color = "#458b74"
jp_font = "Appli Mincho"
txt_color = "black"


def MainWindowStyle():
    return f"""
     QMainWindow {{
        background-image: url('./assets/resource/bg1.jpg'); 
        background-repeat: no-repeat; 
        background-position: center;
    }}
            """


def QProgressBartStyle():
    return f"""
    QProgressBar {{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {main_color};
    width: 20px;
}}
"""


def QListStyle2():
    return f"""
    QListView::item:focus
                {{border:none;}}
    QListWidget
                {{
                border : 0px solid black;
                border-radius:5px;
                background :transparent;
                }}
    QListWidget::item {{ margin: 10px; }}
    QListView::item:selected
                {{
                border : 0px solid 4b86b4;
                background :{main_color};
                border-radius:10px;
                }}
    QListWidget QScrollBar:vertical
                {{
                    background-color: {btn_bg_press_color};
                    width: 10px;
                    margin: 0px 0px 0px 0px;
                    border: 1px transparent #2A2929;
                    border-radius: 5px;
                }}

    QListWidget QScrollBar::handle:vertical
                {{
                    background-color: {main_color};         /* #605F5F; */
                    min-height: 5px;
                    border-radius: 5px;
                }}

    QListWidget QScrollBar::sub-line:vertical
                {{
                    margin: 3px 0px 3px 0px;
                    border-image: url(:/images/up_arrow_disabled.png);        /* # <-------- */
                    height: 10px;
                    width: 10px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                }}

    QListWidget QScrollBar::add-line:vertical
                {{
                    margin: 3px 0px 3px 0px;
                    border-image: url(:/images/down_arrow_disabled.png);       /* # <-------- */
                    height: 10px;
                    width: 10px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                }}

    QListWidget QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
                {{
                    border-image: url(:/images/up_arrow.png);                  /* # <-------- */
                    height: 10px;
                    width: 10px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                }}

    QListWidget QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
                {{
                  
                    height: 10px;
                    width: 10px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                }}
    QListWidget QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
                {{
                    background: none;
                }}

   QListWidget QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
                {{
                    background: none;
                }}
            """


# QTableView{{
#       font-size: 20pt;
#       text-color:{main_color};
#       color:{bg_color};
#       border-radius:15px;
#       alternate-background-color: #E8F8F5 ;
#       border: 0px solid black;
def QTableStyle():
    return f"""
    QTableView
                {{
                   font-size: 25px;
                   alternate-background-color: {btn_bg_press_color} ;
                   border : 2px solid {main_color};
                   border-radius:5px;
                   background:transparent;
                }}
  QScrollBar:vertical
                {{
                    background-color: {btn_bg_press_color};
                    width: 10px;
                    margin: 0px 0px 0px 0px;
                    border: 0px solid {main_color};
                    border-radius: 0px;
                }}

     QScrollBar::handle:vertical
                {{
                    background-color: {main_color};         /* #605F5F; */
                    min-height: 5px;
                    border: 1px solid {main_color};
                    border-radius: 0px;
                }}

     QScrollBar::sub-line:vertical
                {{
                    margin: 3px 0px 3px 0px;
                    border-image: url(:/images/up_arrow_disabled.png);        /* # <-------- */
                    height: 10px;
                    width: 10px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                }}

     QScrollBar::add-line:vertical
                {{
                    margin: 0px 0px 0px 0px;
                    border-image: url(:/images/down_arrow_disabled.png);       /* # <-------- */
                    height: 10px;
                    width: 10px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                }}

     QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
                {{
                    border-image: url(:/images/up_arrow.png);                  /* # <-------- */
                    height: 10px;
                    width: 10px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                }}

    QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
                {{
                  
                    height: 10px;
                    width: 10px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                }}
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
                {{
                    background: none;
                }}

    ScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
                {{
                    background: none;
                }}
    QTableView QTableCornerButton::section 
                {{
                background: {main_color};
                }}
    QTableView::item 
                {{
                border-bottom: 0px solid {main_color};color:{btn_text_color}
                }}
    QTableView::item:selected 
                {{
                 color: white; 
                 background:{main_color}; 
                 font-size: 25px;
                 }}
    QHeaderView::section 
                {{
                color:{bg_color};
                background: {main_color};
                font-size: 25px;
                border-style: none;
                }}
    
    QHeaderView::section:horizontal
    {{
         text-color:{main_color};
         font-size:30px;
    }}
    
    QHeaderView::section:vertical
    {{
         text-color:{main_color};
    }}
 """


def QCheckBoxStyle(font_size=18, border_radius=6, background_color=main_color, border_color=bor_color, width=20,
                   height=20, border_width=2):
    return f"""    
              QCheckBox{{
                          color:{background_color};
                          font-size:{str(font_size)}px;
                          border : 0px solid {bor_color};
                          font:bold;}}  
                          
              QCheckBox::indicator{{
                          border : {str(border_width)}px solid {main_color};
                          width : {str(width)}px;
                          height : {str(height)}px;
                          border-radius :{str(border_radius)}px }}
              
              QCheckBox::indicator:checked {{
                          background-color: {border_color};}}
              QCheckBox:checked, QCheckBox::indicator:checked {{
                          border-color: {border_color} ;
              
              }}
            """


def QRadioButtonStyle(font_size=18, border_radius=11, background_color=txt_color, border_color=main_color, width=20,
                      height=20, border_width=2):
    return f"""    
              QRadioButton{{
                          color:{background_color};
                          font-size:{str(font_size)}px;
                          font:bold;}}  
                          
              QRadioButton::indicator{{
                          border : {str(border_width)}px solid {bor_color};
                          width : {str(width)}px;
                          height : {str(height)}px;
                          border-radius :{str(border_radius)}px }}
              
              QRadioButton::indicator:checked {{
                          background-color: {border_color};}}
              QRadioButton:checked {{
                          border-color: {border_color} ;
            
            """


def QTextEditStyle(text_align="center", background_color=bg_color, height=18, border_radius=10, border_width=1,
                   font_size=20, margin=2):
    return f"""
            QTextEdit {{
                       text-align:{text_align};
                       border : {str(border_width)}px solid {bor_color};
                       background-color: {background_color};
                       border-radius: {str(border_radius)}px;
                       font-size:{str(font_size)}px;
                       margin:{str(margin)}px;
                       height:{str(height)}px;
                       padding:{str(margin)}px;
                       font:bold;}}
        """


def QLineEditStyle(text_align="center", background_color=bg_color, height=50, width=70, border_radius=5, font_size=20,
                   border_width=1, margin=0, margin_left=0):
    return f"""
            QLineEdit {{
                       text-align:{text_align};
                       border : {str(border_width)}px solid {bor_color};
                       background-color: {background_color};
                       border-radius: {str(border_radius)}px;
                       font-size:{str(font_size)}px;
                       margin:{str(margin)}px;
                       margin-left:{str(margin_left)}px;
                       height:{str(height)}px;
                       width:{str(width)}px;
                       padding:{str(margin)}px;
                       font:bold;}}
            
        """


def QComboBoxStyle(background_color=bg_color, border_radius=5, text_color=main_color, font_size=20, margin=0,
                   height=50,
                   width=70, padding=3, border_width=1):
    return f"""
                   QComboBox{{
                       background-color: {background_color};
                       border-radius: {str(border_radius)}px;
                       color: {text_color};
                       font: bold;
                       font-size:{str(font_size)}px;
                       border : {str(border_width)}px solid {bor_color};
                       margin: {str(margin)}px;
                       height:{str(height)}px;
                       width:{str(width)}px;
                       padding:{str(padding)}px;
                   }}
                   
                    QComboBox:editable {{
                        background: Lavender;
                    }}
         
                    QComboBox::drop-down       
                    {{
                    border: 0px; /* This seems to replace the whole arrow of the combo box */
                    }}
                    
                    /* Define a new custom arrow icon for the combo box */
                    QComboBox::down-arrow {{
                    margin-right:10px;
                    image: url(./assets/resource/downward-arrow.png);
                    width: 20px;
                    height: 20px;
                    }}
                QComboBox QAbstractItemView {{
                border: 1px solid Lavender;
                # border-radius: {str(border_radius)}px;
                selection-background-color: Lavender;
}}
                    """


def QPushButtonStyle(text_color=btn_text_color, font_size=18, background_color=btn_bg_color, width=100, height=50,
                     border_radius=10, background_color_pressed=btn_bg_press_color, border_width=1,
                     border_color=bor_color, border_width1=0,
                     background_color_hover=btn_bg_hover_color):
    return f"""
                   QPushButton{{
                       border: {str(border_width1)}px solid {border_color};
                       color: {text_color};
                       font-size:{str(font_size)}px;
                       font:bold;
                       background-color: {background_color};
                       width:{str(width)}px;
                       height:{str(height)}px;
                       border-radius: {str(border_radius)}px;}}
                       QPushButton::pressed{{
                       background-color: {background_color_pressed};
                       width:{str(width)}px;
                       height:{str(height)}px;
                       border-radius: {str(border_radius)}px;}}
                   QPushButton:hover:!pressed
                        {{
                          border: {str(border_width)}px solid {border_color};
                          background-color: {background_color_hover};
                          
                        }}
                   QPushButton:focus
                    {{
                    border: none;
                    outline: none;        
                    }}
            """


def QToolButtonStyle(text_color=btn_text_color, font_size=35, background_color=btn_bg_color, width=300, height=150,
                     border_radius=15, background_color_pressed=btn_bg_press_color, border_width=1,
                     border_color=bor_color,
                     padding_top=20,
                     background_color_hover=btn_bg_hover_color,
                     margin_left=0,
                     margin_top=0):
    return f"""
                   QToolButton{{
                       margin-top:{margin_top}px;
                       color: {text_color};
                       font-size:{str(font_size)}px;
                       font:bold;
                       margin-left:{str(margin_left)}px;
                       padding-top:{str(padding_top)}px;
                       background-color: {background_color};
                       width:{str(width)}px;
                       height:{str(height)}px;
                       border-radius: {str(border_radius)}px;}}
                       QToolButton::pressed{{
                       background-color: {background_color_pressed};
                       width:{str(width)}px;
                       height:{str(height)}px;
                       border-radius: {str(border_radius)}px;}}
                   QToolButton:hover:!pressed
                        {{
                          border: {str(border_width)}px solid {border_color};
                          background-color: {background_color_hover};

                        }}
                   QToolButton:focus
                    {{
                    border: none;
                    outline: none;        
                    }}
            """


def QLabelStyle(text_color=txt_color, font_size=30, font="bold", font_family=jp_font):
    return f"""                   
                    color: {text_color};
                    font-size:{str(font_size)}px;
                    font:{font};
                    font-family:{font_family};

            """


def QLabelStyle_1(text_color=txt_color, font_size=18, font="bold", font_family=jp_font, background_color="white"):
    return f"""                   
                    color: {text_color};
                    font-size:{str(font_size)}px;
                    border-radius: 15px;
                    font:{font};
                    font-family:{font_family};
                    background-color: {background_color};
                    
            """


def QLabelStyleOutLine(text_color=txt_color, font_size=18, font="bold", font_family=jp_font):
    return f"""                   
                    color: {text_color};
                    font-size:{str(font_size)}px;
                    text-outline: 10px 10px #ffffff;
                    font:{font};
                    font-family:{font_family};

            """


def QLabelStyle1(text_color=txt_color, font_size=18, font="bold", font_family=jp_font, background_color="white",
                 border_radius=0, border_width=0):
    return f"""                   
                    color: {text_color};
                    font-size:{str(font_size)}px;
                    font:{font};
                    font-family:{font_family};
                    background-color:{background_color};
                    border-radius:{str(border_radius)}px;
                    border-width:{str(border_width)}px;

            """


def QGroupBoxStyle1(border_width=1, border_color=main_color, border_radius=2, position="top center", padding_title=2,
                    tile_background_color=main_color, title_color="white", background_color="white"):
    return f"""
                    QGroupBox {{
                    border: {str(border_width)}px solid gray;
                    border-color: {border_color};
                    margin-top: 21px;
                    background-color: {background_color};
                    font-size: 17px;
                    font:bold;
                    border-radius: {str(border_radius)}px;
                    border-top-left-radius: 0px;
                    border-top-right-radius: 0px;
                    }}
                    QGroupBox::title {{
                    subcontrol-origin: margin;
                    subcontrol-position: {position};
                    border-top-left-radius: {str(border_radius)}px;
                    border-top-right-radius: {str(border_radius)}px;
                    padding:{str(padding_title)}px 2000px;
                    background-color: {tile_background_color};
                    color: {title_color};
                    }}

             """


def QGroupBoxStyle2(border_width=0, background_color="white", border_color=main_color, border_radius=10,
                    padding_title=2,
                    title_color=txt_color):
    return f"""
                    QGroupBox {{
                    margin:0px;
                    border: {str(border_width)}px solid gray;
                    border-color: {border_color};
                    background-color: {background_color};
                    font:bold;
                    border-radius: {str(border_radius)}px;
                    }}
                    QGroupBox::title {{
                    color: {title_color};
                    background-color: {background_color};
                    subcontrol-origin: margin;
                    padding:{str(padding_title)}px;
                    subcontrol-position: top left;
                    }}
             """


def QGroupBoxHeader(border_width=0, background_color="white", border_color=main_color, border_radius=25,
                    padding_title=2,
                    title_color=txt_color):
    return f"""
                    QGroupBox {{
                    border-bottom-left-radius: {border_radius}px;
                    border-bottom-right-radius: {border_radius}px;
                    border-color: {border_color};
                    background-color: {background_color};
                    font:bold;
                     background-color: 
                       qlineargradient(x1: 0, y1: 0, x2: 0, y2: 0.5, x3: 0 y3: 1,
                                     stop: 0 #ABCD44, stop: 0.5 #ABCD44,
                                     stop: 0.5 #A1C72E, stop: 1.0 #9CC322);
                    }}
             """


def QGroupBoxStyle3(border_width=0, background_color_start="white", border_color=bor_color, border_radius=10,
                    title_color=txt_color, start=0, end=1, background_color_end="Blue"):
    return f"""
                    QGroupBox {{
                    border: {str(border_width)}px solid gray;
                    border-color: {border_color};
                    background-color: {background_color_start};
                    background-color: 
                        qlineargradient(x1: {start},
                                        x2: {end}, 
                                        stop: {start} {background_color_start}, 
                                        stop: {end} {background_color_end});
                    font:bold;
                    border-radius: {str(border_radius)}px;
                    }}
                    QGroupBox::title {{
                    color: {title_color};
                    }}
             """


def QGroupBoxStyle(border_width=1, border_color=main_color, border_radius=10, position="top left", padding_title=2,
                   padding_title_1=20,
                   tile_background_color=main_color, title_color="white", background_color="white", margin_top=21):
    return f"""
                    QGroupBox {{
                    border: {str(border_width)}px solid gray;
                    border-color: {border_color};
                    margin-top: {str(margin_top)}px;
                    background-color: {background_color};
                    font-size: 17px;
                    font:bold;
                    border-radius: {str(border_radius)}px;
                    border-top-left-radius: 0px;
                    }}
                    QGroupBox::title {{
                    subcontrol-origin: margin;
                    subcontrol-position: {position};
                    border-top-left-radius: {str(border_radius)}px;
                    border-top-right-radius: {str(border_radius)}px;
                    padding: {str(padding_title)}px {str(padding_title_1)}px;
                    background-color: {tile_background_color};
                    color: {title_color};
                    }}
                    
             """


def QSliderStyle(border_color=bor_color, back_ground="white", height=15, border_radius=5,
                 back_ground_gradient_0=main_color, ):
    return f"""
            QSlider::groove:horizontal {{
        border: 1px solid {border_color};
        background: {back_ground};
        height: {str(height)}px;
        border-radius: {str(border_radius)}px;
        }}
        
        QSlider::sub-page:horizontal {{
        background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
            stop: 0 {back_ground_gradient_0}, stop: 1 {back_ground_gradient_0});
        background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
            stop: 0 {back_ground_gradient_0}, stop: 1 {back_ground_gradient_0});
        border: 1px solid {back_ground_gradient_0};
        height: 10px;
        border-radius: 4px;
        }}
        
        QSlider::add-page:horizontal {{
        background: #fff;
        border: 1px solid #777;
        height: 10px;
        border-radius: 4px;
        }}
        
        QSlider::handle:horizontal {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #eee, stop:1 #ccc);
        border: 1px solid #777;
        width: 13px;
        margin-top: -2px;
        margin-bottom: -2px;
        border-radius: 4px;
        }}
        
        QSlider::handle:horizontal:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 {back_ground_gradient_0}, stop:1 {back_ground_gradient_0});
        border: 1px solid #444;
        border-radius: 4px;
        }}
        
        QSlider::sub-page:horizontal:disabled {{
        background: #bbb;
        border-color: #999;
        }}
        
        QSlider::add-page:horizontal:disabled {{
        background: #eee;
        border-color: #999;
        }}
        
        QSlider::handle:horizontal:disabled {{
        background: #eee;
        border: 1px solid #aaa;
        border-radius: 4px;
        }}
    
    """
