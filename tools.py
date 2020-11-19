def get_text_from_file(filename):
    with open(filename, 'r') as f:
        text = f.read().lower()
    return text

def get_text_processing(text):
    stop_symbols = [' ', ',']
    return ''.join(j for j in text if not j in stop_symbols)

def get_k_grams_from_text(text, k):
    grams = []
    for i in range(0, len(text)-k+1):
        grams.append(text[i:i+k].lower())
    return grams

def get_hash_from_gram(gram, q):
    h = 0
    k = len(gram)
    for char in gram:
        x = int(ord(char)-ord('a') + 1)
        h = (h * k + x) % q
    return h

def get_hashes_from_grams(grams, q):
    hashes = []
    i = 0
    for gram in grams:
        hashes.append({'value':get_hash_from_gram(gram, q),'index':i})
        i = i + 1
    return hashes

def get_windows(hashes, t):
    k = len(hashes[0])
    w = t - k + 1
    n = len(hashes)
    windows = []
    for i in range(n-w+1):
        windows.append(hashes[i:i+w])
    return windows

def min_(hashes):
    m = hashes[0]
    for i in range(1, len(hashes)):
        if hashes[i]['value'] < m['value']:
            m = hashes[i]
    return m

def find_right(hashes, m):
    for i in range(len(hashes)-1, -1, -1):
        if hashes[i]['value'] == m:
            return hashes[i]

def count_elem(hashes, elem):
    i = 0
    for hash_ in hashes:
        if hash_['value'] == elem:
            i += 1
    return i

def winnow(hashes, t):
    windows = get_windows(hashes, t)

    prints = []
    prev = min_(windows[0])
    prints.append(prev)
    for i in range(1, len(windows)):
        window = windows[i]
        mWindow = min_(window)
        if count_elem(window, mWindow) > 1:
            mWindow = find_right(window, mWindow)
        elif mWindow['value'] == prev['value']:
            continue
        prev = mWindow
        prints.append(prev)
    return prints

def get_fingerprints_with_winnowing(filename, k, q, t):
    text = get_text_from_file(filename)
    print(text)
    text = get_text_processing(text)
    print(text)
    grams = get_k_grams_from_text(text, k)
    print(grams)
    hashes = get_hashes_from_grams(grams, q)
    fingerprints = winnow(hashes, t)
    return fingerprints
