
transform offset_by_time():
    function offset_func(mouth_keyframes)


init python:
    import math

    def play_callback(old, new):
        #renpy.notify(dir(old))
        if(old is not None):
            renpy.notify(renpy.music.get_pos(channel=old.channel))
        renpy.music.play(new._play, channel=new.channel, loop=new.loop, synchro_start=True)
        if new.mask:
            renpy.music.play(new.mask, channel=new.mask_channel, loop=new.loop, synchro_start=True)

    def offset_func(keyframes):
        def f(trans, st, at):
            pos = renpy.music.get_pos(channel="channel")
            if pos is not None:
                offset = interpolate_keyframes(keyframes, pos)
                trans.yoffset = offset
            return 1/24
        return f

    def lerp(a, b, t):
        return a + (b - a) * t

    def cosine_interp(a, b, t):
        ft = t * math.pi
        f = (1 - math.cos(ft)) * 0.5
        return a + (b - a) * f

    def smoothstep(a, b, t):
        t = max(0.0, min(1.0, t))  # clamp
        t = t * t * (3 - 2 * t)
        return a + (b - a) * t

    def ease_in_out_cubic(a, b, t):
        if t < 0.5:
            return a + (b - a) * 4 * t * t * t
        else:
            return a + (b - a) * (1 - (-2*t + 2)**3 / 2)

    def interpolate_keyframes(keyframes, t):
        for i in range(len(keyframes) - 1):
            t0, v0 = keyframes[i]
            t1, v1 = keyframes[i + 1]
            t0 /= 24
            t1 /= 24
            if t0 <= t <= t1:
                f = (t - t0) / (t1 - t0)
                return cosine_interp(v0, v1, f)
        if t < keyframes[0][0]:
            return keyframes[0][1]
        return keyframes[-1][1]

    def get_mouth_lerp_info() -> str:
        global mouth_keyframes
        pos = renpy.music.get_pos(channel="channel")
        if pos is None:
            return ""
        offset = interpolate_keyframes(mouth_keyframes, pos)
        return f"{pos} -> {math.floor(offset)}"


    mouth_keyframes = [
        (0, 20),
        (48, 10),
        (96, 20),
        (144, 10),
        (191, 20),
    ]

