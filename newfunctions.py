def convertStringToList(string):
    string = string.split(", ")
    for i in range(len(string)):
        coord = string[i]
        coord = coord.strip("[")
        coord = coord.strip("]")
        string[i] = coord
    n = len(string) // 2
    newList = []
    for i in range(n):
        newList += [[int(string[2 * i]), int(string[2 * i + 1])]]
            
    return(newList)

newList = convertStringToList("[[53, 31], [493, 58], [65, 239]]")
