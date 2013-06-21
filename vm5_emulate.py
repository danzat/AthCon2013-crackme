def gen_look_up_table():
    for ecx in range(0x100):
        eax = ecx

        for edx in range(8):
            if eax & 1 == 0:
                eax >>= 1
            else:
                eax >>= 1
                eax ^= 0xedb88320

        yield eax

LUT = list(gen_look_up_table())
print '%08X' % LUT[1]

var_406663 = "3C FE FF FF C3 83 7D 16 06 75 0C 83 7D 0A 03 75 2A E8 2A FE FF FF C3 83 7D 16 07 75 1E 83 7D 0A 03 75 18 83 7D 33 40 75 0C 83 7D 0E 00 74 0C E8 0C FE FF FF C3 E8 06 FE FF FF C3 8B 45 1A 01 45 23 83 45 23 02 C3 E8 EE FA FF FF E8 32 FB FF FF 56 A3 DC 4A E8 C4 F8 FF FF 83 7D 0A 03 74 0C E8 C0 FB FF FF C3 E8 BA FB FF FF C3 8B 45 1A 01 45 23 83 45 23 03 C3 E8 EB F8 FF FF 83 7D 16 00 75 15 E8 97 F8 FF FF 83 7D 0A 03 0F 85 A0 00 00 00 E8 8F FB FF FF C3 83 7D 16 01 75 15 E8 7C F8 FF FF 83 7D 0A 03 0F 85 85 00 00 00 E8 74 FB FF FF C3 83 7D 16 02 75 15 E8 61 F8 FF FF 83 7D 0A 03 0F 85 6A 00 00 00 E8 59 FB FF FF C3 83 7D 16 03 75 11 E8 46 F8 FF FF 83 7D 0A 03 75 53 E8 42 FB FF FF C3 83 7D 16 04 75 06 E8 36 FB FF FF C3 83 7D 16 05 75 11 E8 23 F8 FF FF 83 7D 0A 03 75 30"

var_406663 = [int(x, 16) for x in var_406663.split(' ')]
print hex(len(var_406663))

ecx = 0
edi = 0xFFFFFFFF
ptr1 = 0x406663
while ecx < 0xa0:
    eax = var_406663[ecx]
    edx = edi & 0xFF
    eax = eax ^ edx
    ebx = LUT[eax]
    edi >>= 8
    edi = edi ^ ebx
    ecx += 1

print '%08X' % edi
