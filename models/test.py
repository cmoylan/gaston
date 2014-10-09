for quant in range(99, 0, -1):

    #print quant, "bottles of beer on the wall,", quant, "bottles of beer."
    if quant > 2:
        suffix = str(quant - 1) + " bottles of beer on the wall."
    else:
        suffix = "1 bottle of beer on the wall."


    print suffix, suffix
    print "Take one down, pass it around,", suffix
    print "--"
