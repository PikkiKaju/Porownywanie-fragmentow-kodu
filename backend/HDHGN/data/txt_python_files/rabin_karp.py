d = 256
 
def search(pat, txt, q):
    M = len(pat)
    N = len(txt)
    i = 0
    j = 0
    p = 0    
    t = 0    
    h = 1
 
    for i in range(M-1):
        h = (h*d) % q
 
    for i in range(M):
        p = (d*p + ord(pat[i])) % q
        t = (d*t + ord(txt[i])) % q
 
    for i in range(N-M+1):
        if p == t:
            for j in range(M):
                if txt[i+j] != pat[j]:
                    break
                else:
                    j += 1
 
            if j == M:
                print("Pattern found at index " + str(i))
 
        if i < N-M:
            t = (d*(t-ord(txt[i])*h) + ord(txt[i+M])) % q
 
            if t < 0:
                t = t+q