def SimpleCountingSort(arr):
    scope = max(arr) + 1
    C = [0] * scope
    minus_scope = abs(min(arr)) + 1
    B = [0] * minus_scope
    for x in arr:
        if x >= 0:
            C[x] += 1
        else:
            B[abs(x)] += 1
    arr[:] = []
    for number in range(minus_scope):
        arr += [-number] * B[number]
    arr.reverse()
    for number in range(scope):
        arr += [number] * C[number]
    return arr


def main():
    print(SimpleCountingSort([30220180, 11897874, 30485241, 98895363, 35071568, 49460507, 98676250, 63229133, -6510118, 13017380, 33097017, 19719663]))


if __name__ == '__main__':
    main()
