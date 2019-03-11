from PIL import ImageGrab

BLACK = (0, 0, 0)
LOW_THRESHOLD = 40
MID_THRESHOLD = 60
HIGH_THRESHOLD = 230

def most_frequent_colour(image):

    w, h = image.size
    pixels = image.getcolors(w * h)

    most_frequent_pixel = pixels[0]

    for count, colour in pixels:
        if count > most_frequent_pixel[0] and colour != BLACK:
            most_frequent_pixel = (count, colour)

    rgb = most_frequent_pixel[1]

    return rgb

def image_bloom_colour(img):
    img = img.resize((100, 41))
    dark_pixels = 1
    mid_range_pixels = 1
    total_pixels = 1
    r = 1
    g = 1
    b = 1

    # Win version of imgGrab does not contain alpha channel
    if img.mode == 'RGB':
        img.putalpha(0)

    # Create list of pixels
    pixels = list(img.getdata())

    for red, green, blue, alpha in pixels:
        # Don't count pixels that are too dark
        if red < LOW_THRESHOLD and green < LOW_THRESHOLD and blue < LOW_THRESHOLD:
            dark_pixels += 1
        # Or too light
        elif red > HIGH_THRESHOLD and green > HIGH_THRESHOLD and blue > HIGH_THRESHOLD:
            pass
        else:
            if red < MID_THRESHOLD and green < MID_THRESHOLD and blue < MID_THRESHOLD:
                mid_range_pixels += 1
                dark_pixels += 1
            r += red
            g += green
            b += blue
        total_pixels += 1

    n = len(pixels)
    r_avg = r / n
    g_avg = g / n
    b_avg = b / n
    rgb = [r_avg, g_avg, b_avg]

    # If computed average below darkness threshold, set to the threshold
    for index, item in enumerate(rgb):
        if item <= LOW_THRESHOLD:
            rgb[index] = LOW_THRESHOLD

    rgb = (int(rgb[0]), int(rgb[1]), int(rgb[2]))

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
