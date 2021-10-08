# Global settings
__version__ = '1.1'

# Root settings
WIDTH = 900
HEIGHT = 500

MIN_SIZE = (900, 500)
MAX_SIZE = (1100, 700)

ROOT_RESIZABLE = (True, True)

ROOT_TITLE = "SQLite Browser"

RELIEF = 'flat'
FONT = 'Arial 16'

# Base settings
DB_NAME = ''

FILE_TYPES = [
    ('SQLite', '*.db *.sqlite'),
    ('Все файлы', '*')
]

# All windows names
WINDOWS = ['MAIN', 'DATA']

# Theme
NOW_LIGHT_THEME = True

THEME_LIGHT = {
    'FRAME': '#D9D9D9',
    'BUTTON': '#D9D9D9',
    'ACTIVE': '#E9E9E9',
    'TEXT': '#FFFFFF',
    'LABEL': '#FFFFFF',
    'BORDER': '#666666',
    'FG': '#000000',
    'ERROR': '#FF0000',
    'THEME': '\U0001F312',  # Moon Emoji for theme_button
    'COMBOBOX': {
        'BACKGROUND': '#FFFFFF',
        'FOREGROUND': '#000000',
        'SBACKGROUND': '#CFCFCF',
        'SFOREGROUND': '#000000',
        'SETTINGS': {
            'TCombobox': {
                'configure': {
                    'selectbackground': '#FFFFFF',
                    'selectforeground': '#000000',
                    'fieldbackground': '#FFFFFF',
                    'background': '#B0B0B0',
                    'foreground': '#000000',
                }
            }
        }
    }
}

THEME_DARK = {
    'FRAME': '#282828',
    'BUTTON': '#444444',
    'ACTIVE': '#777777',
    'TEXT': '#444444',
    'LABEL': '#444444',
    'BORDER': '#555555',
    'FG': '#FFFFFF',
    'ERROR': '#FF0000',
    'THEME': '\U0001F316',  # Sun Emoji for theme_button
    'COMBOBOX': {
        'BACKGROUND': '#444444',
        'FOREGROUND': '#FFFFFF',
        'SBACKGROUND': '#666666',
        'SFOREGROUND': '#FFFFFF',
        'SETTINGS': {
            'TCombobox': {
                'configure': {
                    'selectbackground': '#444444',
                    'selectforeground': '#FFFFFF',
                    'fieldbackground': '#444444',
                    'background': '#444444',
                    'foreground': '#FFFFFF',
                }
            }
        }
    }
}