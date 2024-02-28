init python:
    def get_zoom(zposition=0):
        return round(map_value(zposition), 3)

    #to handle zoom levels for 21:9 display
    def map_value(x):
        known_points = {
            -1000 : 1.05,
            -500 : 1.06,
            -300 : 1.07,
            0 : 1.1,
            500 : 1.13,
            700 : 1.18,
            800 : 1.22,
            900 : 1.28,
            1000 : 1.4
        }

        nearest_lower = max(k for k in known_points.keys() if k <= x)
        nearest_higher = min(k for k in known_points.keys() if k >= x)

        output = log_interp(x, nearest_lower, nearest_higher, known_points[nearest_lower], known_points[nearest_higher])

        return output

    def log_interp(x, x0, x1, y0, y1):
        if x0 == x1:
            return (y0 + y1) / 2
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        return y0 * ((x1 - x) / (x1 - x0)) + y1 * ((x - x0) / (x1 - x0))


    def moving_camera(trans, st, at):
        if parallax_on:
            x, y = renpy.display.draw.get_mouse_pos()

            parallax_factor = 0.055
            target_xoffset = (x - config.screen_width / 2) * parallax_factor
            target_yoffset = (y - config.screen_height / 2) * parallax_factor

            easing_factor = 0.055 #closer to 0 = slower, closer to 1 = faster, with 1 being no ease
            trans.xoffset += (target_xoffset - trans.xoffset) * easing_factor
            trans.yoffset += (target_yoffset - trans.yoffset) * easing_factor
        else:
            trans.xoffset = 0
            trans.yoffset = 0

        return 0

transform parallax:
    perspective True
    subpixel True
    function moving_camera

#handles values between -1000 (far away) and 1000 (SUPER close)
transform depth(zposition=0):
    truecenter()
    zpos zposition
    zzoom True
    xzoom get_zoom(zposition)
    yzoom get_zoom(zposition)


label start:
    camera at parallax
    show SomeImage at depth(-500)
    show SomeOtherImage at depth(-300)
    show YetAnotherImage at depth(-100)
