def getMetadata(path, bbox=False, time = False):
    if bbox == 'bbox' and time == True :
        return "dummy bbox and time"
    elif bbox == 'bbox' and time == False :
        return "dummy bbox"
    elif bbox == False and time == True :
        return "dummy time"
    