def row2dict(lst, rows):
    mp = {}
    rows = zip(*rows)
    for i,j in enumerate(lst):
        mp[j] = rows[i]
    return mp

if __name__ == '__main__':
    print zip([['a','b','c'],['d','e','f']])
    print row2dict([1,2,3], [['a','b','c'],['d','e','f']])