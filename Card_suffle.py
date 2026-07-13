def card_shuffle(L):
    n = len(L) // 2

    L1 = L[:n]
    L2 = L[n:]

    result = []

    for i in range(n):
        result.append(L1[i])
        result.append(L2[i])

    return result


L = [1,2,3,4,5,6,7,8]
print(card_shuffle(L))