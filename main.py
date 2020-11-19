from tools import get_fingerprints_with_winnowing
k = 5  # Размер k-грамм
q = 31
t = 8

file1 = 'test1.cpp'
file2 = 'test2.cpp'
prints1 = get_fingerprints_with_winnowing(file1, k, q, t)
prints2 = get_fingerprints_with_winnowing(file2, k, q, t)



