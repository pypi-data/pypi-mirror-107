def union(list1, list2):
    data = set(list1) | set(list2)
    return data

def getOffsetFromRef(pixels_off, ref, BLOCK_SIZE):
    return abs(pixels_off - ref) % BLOCK_SIZE

def display(width, height):
    return pygame.display.set_mode((width, height))
