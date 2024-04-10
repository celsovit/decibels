# https://testdriven.io/blog/django-charts/

months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
weekdays = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
colors_names = ['lightRed', 'lightBlue', 'lightYellow', 'lightCyan', 'lightPurple', 'lightOrange', 'lightGreen']

colorPalette = [
    'rgba(255, 99, 132, 0.5)',  # Light Red
    'rgba(54, 162, 235, 0.5)',  # Light Blue
    'rgba(255, 206, 86, 0.5)',  # Light Yellow
    'rgba(75, 192, 192, 0.5)',  # Light Cyan
    'rgba(153, 102, 255, 0.5)', # Light Purple
    'rgba(255, 159, 64, 0.5)',  # Light Orange
    'rgba(0, 204, 102, 0.5)',   # Light Green
]

for name, color in zip(colors_names, colorPalette):
    locals()[name] = color


def get_year_dict():
    year_dict = dict()

    for month in months:
        year_dict[month] = 0

    return year_dict


def generate_color_palette(amount):
    palette = []

    i = 0
    while i < len(colorPalette) and len(palette) < amount:
        palette.append(colorPalette[i])
        i += 1
        if i == len(colorPalette) and len(palette) < amount:
            i = 0

    return palette

