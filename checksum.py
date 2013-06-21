rol=lambda x, y: (x << y) & 0xFFFFFFFF | ((x & 0xFFFFFFFF) >> (32-y%32))

def checksum(string):
    cs = 0
    for c in string:
        l = rol(ord(c), 7)
        cs = rol(cs + l, 7)
        cs = cs ^ l
    cs = cs ** 2 & 0xFFFFFFFFFFFFFFFF
    cs_hi = cs / (2**32)
    cs_lo = cs % (2**32)
    return (cs_lo + cs_hi) & 0xFFFFFFFF

if __name__ == '__main__':
    from sys import argv
    if len(argv) == 2:
        with open(argv[1], 'rU') as names_file:
            for line in names_file.readlines():
                print hex(checksum(line.strip())), line.strip()
