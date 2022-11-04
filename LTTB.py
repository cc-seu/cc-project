import math


def tri_area(x1, y1, x2, y2, x3, y3):
    return 0.5 * abs(x2 * y3 + x1 * y2 + x3 * y1 - x3 * y2 - x2 * y1 - x1 * y3)


def LTTB(data, threshold):
    l = len(data)
    buckets = []
    first = []
    last = []
    first.append(data[0])
    last.append(data[l - 1])
    buckets.append(first)
    num = (l - 2) // (threshold - 2)
    mod = (l - 2) % (threshold - 2)
    for i in range(0, mod):
        bucket = []
        for j in range(1, num + 2):
            bucket.append(data[i * (num + 1) + j])
        buckets.append(bucket)
    for i in range(mod, threshold - 2):
        bucket = []
        for j in range(1, num + 1):
            bucket.append(data[i * num + mod + j])
        buckets.append(bucket)
    buckets.append(last)
    F_point = []
    F_point.append(buckets[0][0])
    for i in range(1, threshold - 1):
        l_next = len(buckets[i + 1])
        next_sum = 0
        for k in range(0, l_next):
            next_sum += buckets[i + 1][k]
        next = next_sum / l_next
        pre = F_point[i - 1]
        l_cur = len(buckets[i])
        S = []
        for m in range(0, l_cur):
            S.append(tri_area(1, pre, 2, buckets[i][m], 3, next))
        F_point.append(buckets[i][S.index(max(S))])
    F_point.append(last[0])

    return F_point
