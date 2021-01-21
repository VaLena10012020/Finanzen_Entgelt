from os import path
from glob import glob


def find_ext(dr, ext, ig_case=False):
    if ig_case:
        ext =  "".join(["[{}]".format(
                ch + ch.swapcase()) for ch in ext])
    return glob(path.join(dr, "*." + ext))