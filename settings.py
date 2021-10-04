# Global settings
__version__ = '0.3'

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
    'ERROR': '#FF0000'
}

THEME_DARK = {
    'FRAME': '#282828',
    'BUTTON': '#444444',
    'ACTIVE': '#777777',
    'TEXT': '#444444',
    'LABEL': '#444444',
    'BORDER': '#555555',
    'FG': '#FFFFFF',
    'ERROR': '#FF0000'
}