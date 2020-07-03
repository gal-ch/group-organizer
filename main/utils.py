import time

def domesday(area):
    start_time = time.time()
    arr = []
    new_area = area
    digit = [3, 9, 31, 99, 316, 999, 1000]
    count = 0
    while new_area != 0:
        new_area //= 10
        count += 1
    i = digit[count - 1]
    while area != 0:
        while area < i * i:
            i -= 1
        area = area - i * i
        arr.append(i * i)
    print(84532 // 1000)
    print(area)
    print(arr)
    print("--- %s seconds1 ---" % (time.time() - start_time))

domesday(15324)


def largestSquare(area):
    time1 = 0.00018668174743652344
    time2 = 6.318092346191406e-05
    if time2 < time1:
        print(time2)
    start_time = time.time()
    arr = []
    while area != 0:
        i = 0
        while (i+1)*(i+1) <= area:
            i += 1
        area = area - i * i
        arr.append(i * i)
    print(area)
    print(arr)
    print("--- %s seconds2 ---" % (time.time() - start_time))


largestSquare(15324)