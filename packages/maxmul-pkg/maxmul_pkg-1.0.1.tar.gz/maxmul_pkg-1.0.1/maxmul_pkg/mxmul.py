def mxmul(mix1, mix2, nrow, nk, ncol):
    rst = [[0 for x in range(ncol)] for y in range(nrow)]
    for i in range(nrow):
        for j in range(ncol):
            for k in range(nk):
                rst[i][j] += mix1[i][k] * mix2[k][j]
    return rst


def mxsum(mx, nrow, ncol):
    s = 0
    for i in range(nrow):
        for j in range(ncol):
            s += mx[i][j]
    return s


if __name__ == "__main__":
    import time

    nrow, nk, ncol = 2, 5, 3
    mix1 = [[y for y in range(nk)] for x in range(nrow)]
    mix2 = [[y for y in range(ncol)] for x in range(nk)]
    start = time.perf_counter()
    muul = mxmul(mix1, mix2, nrow, nk, ncol)
    end = time.perf_counter()
    print(muul)
    print("{:.4f}".format(end - start))
    # .4f保留小数点后四位
