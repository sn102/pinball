def endScreen(pinballGroup):
    if pinballGroup.sprites()[0].getScore() > pinballGroup.sprites()[1].getScore():
        endText = ("Player 1 wins!")
    elif pinballGroup.sprites()[1].getScore() > pinballGroup.sprites()[0].getScore():
        endText = ("Player 2 wins!")
    else:
        endText = ("Draw!")
        pinballGroup.empty()
    return(endText)
