import darkdetect

theme = darkdetect.theme()

colors = {
    'primary': '#101010' if theme == 'Dark' else '#ffffff',
    'secondary': '#008f5b',
    'shade': '#232323' if theme == 'Dark' else '#d2d2d2',
}
