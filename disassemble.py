import re
import struct
import subprocess
from cStringIO import StringIO

def load_opcode_dict(filename):
    with open(filename, 'rU') as infile:
        return dict(line.strip().split(';') for line in infile.readlines() if line[0] != '#')

def process(instruction, stream):
    if instruction.find('rel8') > 0:
        operand = stream.read(1)
        rel8, = struct.unpack('<b', operand)
        return instruction.replace('rel8', hex(rel8)), operand.encode('hex')
    elif instruction.find('imm8') > 0:
        operand = stream.read(1)
        imm8, = struct.unpack('<B', operand)
        return instruction.replace('imm8', hex(imm8)), operand.encode('hex')
    elif instruction.find('rel32') > 0:
        operand = stream.read(4)
        rel32, = struct.unpack('<l', operand)
        return instruction.replace('rel32', hex(rel32)), operand.encode('hex')
    elif instruction.find('imm32') > 0:
        operand = stream.read(4)
        imm32, = struct.unpack('<L', operand)
        return instruction.replace('imm32', hex(imm32)), operand.encode('hex')
    else:
        return instruction, ''

def is_opcode_in_table(opcode_lo, opcode_dict):
    opcode_lo_hex = chr(ord(opcode_lo) ^ 0x8a).encode('hex')
    return opcode_lo_hex in [key[:2] for key in opcode_dict.keys()]

def disassemble_native(stream, uncharted_opcode_translation_table, stream_end, address):
    raw_opcode = stream.read(1)
    try:
        opcode_lo = chr(uncharted_opcode_translation_table.find(raw_opcode))
    except:
        s = raw_input('current address is %08X. How many bytes to skip?: ' % address)
        stream.read(int(s))
        return ''
    # Try to find the opcode in the opcodes dict
    opcode_str = opcode_lo.encode('hex')
    while stream.tell() < stream_end:
        rasm2 = subprocess.Popen(['rasm2', '-d', opcode_str], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        stdout, stderr = rasm2.communicate()
        if stderr != '':
            opcode_str += stream.read(1).encode('hex')
        else:
            return '%08X % 16s %s' % (address, opcode_str, stdout.strip(), )
    return ''

class IllegalBytecode(Exception): pass

def disassemble_bytecode(stream, opcode_dict, address):
    opcode_lo = stream.read(1)
    opcode_lo_unxored = chr(ord(opcode_lo) ^ 0x8A)
    # Try to find the opcode in the opcodes dict
    opcode_lo_str = opcode_lo_unxored.encode('hex')
    if opcode_lo_str in opcode_dict:
        instruction = opcode_dict[opcode_lo_str]
        opcode_hex = opcode_lo.encode('hex')
    else:
        opcode_hi = stream.read(1)
        opcode_str = opcode_lo_str + opcode_hi.encode('hex')
        opcode_hex = (opcode_lo + opcode_hi).encode('hex')
        if opcode_str in opcode_dict:
            instruction = opcode_dict[opcode_str]
        else:
            stream.seek(-2, 1) # rewind
            raise IllegalBytecode
    mnemonic, operand = process(instruction, stream)
    return '%08X % 16s %s' % (address, opcode_hex + operand, mnemonic, )

def __disassemble(code, mask, opcode_dict, start_address):
    stream = StringIO(code)
    uncharted_opcode_translation_table = open('vm1_uncharted_opcode_translation.txt', 'rU').read().strip().decode('hex')
    disallow_masking = [line.strip() for line in open('vm2_require_nativity_mask.txt', 'rU').readlines()]
    while stream.tell() < len(code):
        opcode_lo = stream.read(1)
        stream.seek(-1, 1)
        if is_opcode_in_table(opcode_lo, opcode_dict):
            if chr(ord(opcode_lo) ^ 0x8a).encode('hex') not in disallow_masking:
                if mask[stream.tell()] == '\x00':
                    yield disassemble_native(stream, uncharted_opcode_translation_table, len(code), start_address + stream.tell())
                else:
                    try:
                        yield disassemble_bytecode(stream, opcode_dict, start_address + stream.tell())
                    except IllegalBytecode:
                        yield disassemble_native(stream, uncharted_opcode_translation_table, len(code), start_address + stream.tell())
            else:
                try:
                    yield disassemble_bytecode(stream, opcode_dict, start_address + stream.tell())
                except IllegalBytecode:
                    yield disassemble_native(stream, uncharted_opcode_translation_table, len(code), start_address + stream.tell())
        else:
            yield disassemble_native(stream, uncharted_opcode_translation_table, len(code), start_address + stream.tell())

def disassemble(code, mask, opcode_dict, start_address, call_offset):
    jump_regex = re.compile('([0-9A-F]+)\s+([0-9a-f]+) j[^\s]+ (-?0x[0-9a-f]+)')
    call_regex = re.compile('([0-9A-F]+)\s+([0-9a-f]+) call (-?0x[0-9a-f]+)')
    for line in __disassemble(code, mask, opcode_dict, start_address):
        jump_match = jump_regex.match(line)
        call_match = call_regex.match(line)
        if jump_match is not None:
            base_address, instruction_hex, offset = jump_match.groups()
            target_address = int(base_address, 16) + len(instruction_hex) / 2 + int(offset, 16)
            print line, '(%08X)' % target_address
        elif call_match is not None:
            base_address, instruction_hex, offset = call_match.groups()
            target_address = int(base_address, 16) + len(instruction_hex) / 2 + int(offset, 16) - call_offset
            print line, '(%08X)' % target_address
        else:
            print line

if __name__ == '__main__':
    from sys import argv
    
    if len(argv) != 5:
        print 'USAGE: %s <code filename> <mask filename> <start address> <call offset>' % argv[0]
    else:
        code = open(argv[1], 'rU').read().strip().decode('hex')
        mask = open(argv[2], 'rU').read().strip().decode('hex')
        start_address = int(argv[3], 16)
        call_offset = int(argv[4], 16)
        opcode_dict = load_opcode_dict('vm1_opcodes.txt')
        disassemble(code, mask, opcode_dict, start_address, call_offset)
