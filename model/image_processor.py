from PIL import ImageGrab
from .k_means_processor import DominantColors

BLACK = (0, 0, 0)

def most_frequent_colour(image):

    w, h = image.size
    pixels = image.getcolors(w * h)

    most_frequent_pixel = pixels[0]

    for count, colour in pixels:
        if count > most_frequent_pixel[0] and colour != BLACK:
            most_frequent_pixel = (count, colour)

    rgb = most_frequent_pixel[1]

    return rgb

def scored_frequent_colour(image):
    w, h = image.size
    pixels = image.getcolors(w * h)

    most_frequent_pixel = pixels[0]

    for count, colour in pixels:
        if count > most_frequent_pixel[0] and colour != BLACK:
            most_frequent_pixel = (count, colour)

    rs = 0
    gs = 0
    bs = 0
    r,g,b = most_frequent_pixel[1] # EG (125, 255, 0)

    # Scoring Red vs Green
    if r <= g:
        gs += 1
        if r == g:
            rs += 1
    else:
        rs += 1

    # Scoring Red vs Blue
    if r <= b:
        bs += 1
        if r == b:
            rs += 1
    else:
        rs += 1

    # Scoring Green vs Blue
    if g <= b:
        bs += 1
        if g == b:
            gs += 1
    else:
        gs += 1

    def scoring(val):
        if val == 0:
            return 0
        elif val == 1:
            return 125
        else:
            return 255

    rgb = (scoring(rs), scoring(gs), scoring(bs))

    return rgb

def kmeans_colour(image):
    dc = DominantColors(image, 3)
    colors = dc.dominantColors()

    rgb = (colors[2][0], colors[2][1], colors[2][2])
    return rgb
