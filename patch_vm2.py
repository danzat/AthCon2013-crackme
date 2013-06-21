corrections = [(0x424b7b, 0x424bc6),
               (0x424bed, 0x424c3a),
               (0x424c74, 0x424ca2),
               (0x424ca7, 0x424cdd),
               (0x424cfc, 0x424d32),
               (0x424da5, 0x424ddd),
               (0x424de3, 0x424e1b),
               (0x424e38, 0x424e68),
               (0x424e6d, 0x424ea1),
               (0x424ec2, 0x424ef2),
               (0x424ef7, 0x424f2b),
               (0x424f4e, 0x424f82),
               (0x424fdc, 0x425010),
               (0x425068, 0x4250a2),
               (0x4250a8, 0x4250dc),
               (0x4250fd, 0x425133),
               (0x425138, 0x42516a),
               (0x42518b, 0x4251bf),
               (0x4251c4, 0x4251fb),
               (0x425263, 0x4252e5),
               (0x42531d, 0x42536b),
               (0x4253a4, 0x4253da),
               (0x425400, 0x425436),
               (0x425476, 0x4254a8),
               (0x4254da, 0x425528),
               (0x425537, 0x425569),
               (0x4255e7, 0x425623),
               (0x42562e, 0x425668),
               (0x425670, 0x4256aa),
               (0x425731, 0x425769),
               (0x425774, 0x4257ae),
               (0x4257b6, 0x4257f0),
               (0x425822, 0x42586f),
               (0x425886, 0x4258ba),
               (0x4258fa, 0x425934),
               (0x4259b3, 0x4259ff),
               (0x425a49, 0x425aed),
               (0x425b26, 0x425b5a),
               (0x425bb4, 0x425be8),
               (0x425c2b, 0x425c5f),
]

xor_eaxs = [0x424cf8, 0x424f4a, 0x4258fa, 0x425b22]

BASE_VA = 0x424ADE
BASE_FILE_OFFSET = 0x224DE

if __name__ == '__main__':
    with open('ATHCON_2013_RE_CHALLENGE.exe', 'rb') as infile:
        file_str = infile.read()
        file_arr = map(ord, file_str)
    for eip_from, eip_to in corrections:
        file_offset = BASE_FILE_OFFSET + eip_from - BASE_VA
        jump_offset = eip_to - eip_from - 2
        file_arr[file_offset] = 0xd6
        file_arr[file_offset + 1] = jump_offset
    for eip in xor_eaxs:
        file_offset = BASE_FILE_OFFSET + eip - BASE_VA
        file_arr[file_offset] = 0x40
        file_arr[file_offset + 1] = 0x01
    with open('ATHCON_2013_RE_CHALLENGE_patched.exe', 'wb') as outfile:
        outfile.write(''.join(chr(x) for x in file_arr))
