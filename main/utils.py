

def domesday(area):
    arr = []
    total = 0
    num = 100
    while num < 150:
        double = num * num
        if double <= area < double + (num + (num * 2)):
            arr.append(double)

            num = area - double
    print(arr)

domesday(15324)