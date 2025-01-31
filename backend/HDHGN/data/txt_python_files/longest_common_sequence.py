def lcs(s1, s2, m, n):
    if m == 0 or n == 0:
        return 0

    if s1[m - 1] == s2[n - 1]:

        return 1 + lcs(s1, s2, m - 1, n - 1)

    else:
        return max(lcs(s1, s2, m, n - 1), lcs(s1, s2, m - 1, n))

if __name__ == "__main__":
    s1 = "AGGTAB"
    s2 = "GXTXAYB"
    m = len(s1)
    n = len(s2)

    print(lcs(s1, s2, m, n))