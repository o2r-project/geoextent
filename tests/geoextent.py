def getMetadata(path, bbox=False, time = False):
    if bbox == 'bbox' and time == 'Time' :
        return "dummy bbox and time"
    elif bbox == 'bbox' and time == False :
        return "dummy bbox"
    elif bbox == False and time == 'Time' :
        return "dummy time"
    