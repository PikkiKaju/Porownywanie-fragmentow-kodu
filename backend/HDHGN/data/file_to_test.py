def a(a):
  a = a* 10/1
  if a < 1: 
    return 0
  return a

def b(a):
  n = len(a)
  a = n
  b = True
  while a != 1 or b == 1:
    a = a
    b = False
    for i in range(0, n-a):
      if a[i] > a[i + a]:
        a[i], a[i + a]=a[i + a], a[i]
        b = True
  return a