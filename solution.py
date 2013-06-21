hardcoded = [0x8df489ac, 0x0c9aef51, 0x9dca468b, 0x09ae2b76]

target_eip = 0x40d44e

delta = 0x4e1a9001

#vm2_delta = 0x1804000d
vm2_delta = 0x1624000d

# file[0] ^ file[1] ^ file[2] ^ file[3] ^ (hardcoded[0] + 14 * vm2_delta) ^ (hardcoded[1] + 14 * vm2_delta) ^ (hardcoded[2] + 15 * vm2_delta) ^ (hardcoded[3] + 15 * vm2_delta) - delta = target_eip
# file[0] = file[1] = file[2] = 0xffffffff ; I can make an arbitrary choice

ebx = ecx = edx = 0xffffffff
eax = ebx ^ ecx ^ edx ^ (hardcoded[0] + vm2_delta * 14) ^ (hardcoded[1] + vm2_delta * 14) ^ (hardcoded[2] + vm2_delta * 15) ^ (hardcoded[3] + vm2_delta * 15) ^ (target_eip + delta)

print hex(eax)
