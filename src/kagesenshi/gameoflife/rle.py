# http://www.conwaylife.com/wiki/RLE


def decode(rlestring):
    '''
    >>> from pprint import pprint
    >>> beacon = 'x = 6, y = 6\n2o2b$o3b$3bo$2b2o!'
    >>> pprint(decode(beacon))
    [(1, 1, 0, 0, 0, 0),
     (1, 0, 0, 0, 0, 0),
     (0, 0, 0, 1, 0, 0),
     (0, 0, 1, 1, 0, 0),
     (0, 0, 0, 0, 0, 0),
     (0, 0, 0, 0, 0, 0)]
    '''

    s = filter(lambda x: not x.startswith('#'), rlestring.strip().split('\n'))
    # decode first line
    xsize,ysize = s[0].replace(',','').replace('x','').replace('y','').replace('=','').split()
    xsize,ysize = int(xsize), int(ysize)
    body = ''.join(s[1:])

    row = []
    res = []
    size = ''
    for char in body:
        if char in ['o','b']:
            if not size:
                size = '1'
            if char == 'o':
                row += int(size)*(1,)
            elif char == 'b':
                row += int(size)*(0,)
            size = ''
        elif char in ['$','!']:
            if len(row) < xsize:
                row += (xsize-len(row))*(0,)
            res.append(tuple(row))
            row = []
        else:
            size += char
    if len(res) < ysize:
        row = (0,)*xsize
        res += (row,)*(ysize-len(res))
    return res

if __name__ == '__main__':
    from pprint import pprint
    pprint(decode('x = 6, y = 6\n2o2b$o3b$3bo$2b2o!'))
