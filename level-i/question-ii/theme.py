import darkdetect

theme = darkdetect.theme()

colors = {
    'background': '#101010' if theme == 'Dark' else '#ffffff',
    'shade': '#232323' if theme == 'Dark' else '#d2d2d2',
    'green': '#008f5b',
    'yellow': '#ffff4d',
}
