'''
We are adding two binary numbers.
On each bit pair, we have this circuit:
    z_0 = x_0 XOR y_0
    carry_0 = x_0 AND y_0
    z_n = x_n XOR y_n XOR carry_(n-1)
    carry_n = (x_n AND y_n) OR ((carry_(n-1) AND (x_n XOR y_n))

'''

import importlib
day_24_01 = importlib.import_module('a-24-01')

class Gate(day_24_01.Gate):
    def __hash__(self) -> int:
        return hash(tuple([self.in1,self.in2,self.gate_type_name])) + hash(tuple([self.in2,self.in1,self.gate_type_name]))

class Wire:
    def __init__(self, name: str, value: int) -> None:
        self.name = name
        self.value = value # 0 or 1 or -1 for no value
        self.index = -1 # just to iniatilize value
        if name[1].isdigit() and name[2].isdigit():
            self.add_type_and_index(name[0], int(name[1:]))
    def __repr__(self) -> str:
        if self.index != -1:
            return f'Wire: Name {self.name}, Value {self.value}, Index {self.index}, Type {self.type_name}'
        return f'Wire: Name {self.name}, Value {self.value}'
    def add_type_and_index(self, type_name: str, index: int) -> None:
        '''
        possible indices: 0...44
        possible types:
          x,y for input
          z for output
          m for "x_n XOR y_n"
          n for "x_n AND y_n"
          o for "m_n AND c_(n-1)"
          c for carry bit "n_n AND o_n"
        '''
        self.type_name = type_name
        self.index = index

class Circuit(day_24_01.Circuit):
    def __init__(self, input_filename: str) -> None:
        with open(input_filename, 'r') as f:
            lines = f.readlines()
        start_wires, gates = ''.join(lines).split('\n\n')
        wire_dict = {}
        gate_list = []

        for line in start_wires.split('\n'):
            print(line)
            wire_name, wire_value = line.split(':')[0], int(line.split(':')[1].strip())
            wire_dict.update({wire_name: Wire(wire_name, wire_value)})
        self.wire_dict = wire_dict

        for line in gates.split('\n'):
            if line.strip() == '': continue
            in1, gate_type, in2, _, out = line.split()
            if in1 not in self.wire_dict:
                self.wire_dict[in1] = Wire(in1, -1)
            if in2 not in self.wire_dict:
                self.wire_dict[in2] = Wire(in2, -1)
            if out not in self.wire_dict:
                self.wire_dict[out] = Wire(out, -1)

            in1, in2 = sorted([in1,in2])
            wire_in1 = self.wire_dict.get(in1)
            wire_in2 = self.wire_dict.get(in2)
            wire_out = self.wire_dict.get(out)
            print(wire_in2)
            gate_list.append(Gate(wire_in1, wire_in2, wire_out, gate_type))

        self.gates = gate_list
        print(self.gates)
        print(self.wire_dict)

    def make_translation(self) -> None:
        for gate in self.gates:
            if -1 in (gate.in1.index, gate.in2.index):
                continue
            in1, in2, out, gate_type_name = gate.in1, gate.in2, gate.out, gate.gate_type_name
            if (in1.type_name, in2.type_name, gate_type_name) == ('x','y','XOR'):
                if in1.index == 0:
                    gate.out.add_type_and_index('z',0)
                else:
                    gate.out.add_type_and_index('m',in1.index)
            elif (in1.type_name, in2.type_name, gate_type_name) == ('x','y','AND'):
                if in1.index == 0:
                    gate.out.add_type_and_index('c',0)
                else:
                    gate.out.add_type_and_index('n',in1.index)
        for wire_name, wire in self.wire_dict.items():
            print(wire)

    def find_x_y_wires(self):
        self.x_wires = []
        self.y_wires = []
        for wire_name,wire in self.wire_dict.items():
            if wire.value == -1: continue
            if wire_name.startswith('x'):
                self.x_wires.append(wire_name)
            elif wire_name.startswith('y'):
                self.y_wires.append(wire_name)
        self.x_wires = sorted(self.x_wires)
        self.y_wires = sorted(self.y_wires)

    def check_xor(self) -> list:
        xors_to_check = [(x,y,'XOR') for x,y in zip(self.x_wires, self.y_wires)]
        print(xors_to_check)
        hashed_gates = [hash(gate) for gate in self.gates]
        for check in xors_to_check:
            x,y,value = check
            if hash(Gate(x,y,'9999','XOR')) in hashed_gates:
                print(x,y)

def read_wires(input_filename: str) -> list[tuple[str]]:
    with open(input_filename, 'r') as f:
        lines = ''.join(f.readlines())

    input_list = []
    inputs, wires = lines.split('\n\n')
    for input_line in inputs.split('\n'):
        input_list.append(input_line.split(':')[0])

    wire_list = []
    print(wires)
    for line in wires.split('\n'):
        if line == '':
            continue
        print(line)
        in1, gate_type, in2, _, out = line.split()
        wire_list.append((in1,in2,gate_type,out))

    return input_list, wire_list

def sort_wire_list(wire_list) -> list[Wire]:
    new_wire_list = []
    for w in wire_list:
        sorted_inputs = sorted(w[:2])
        sorted_inputs.append(w[2])
        sorted_inputs.append(w[3])
        new_wire_list.append(tuple(sorted_inputs))
    return sorted(new_wire_list)

def make_translation(wire_list) -> list[tuple[str]]:
    translation_dict = {f'x{i:02d}': f'x{i:02d}' for i in range(45)}
    translation_dict.update({f'y{i:02d}': f'y{i:02d}' for i in range(45)})
    wires_to_check = wire_list[:]

    while len(wires_to_check) > 0:
        wire_to_check = wires_to_check.pop()
        print(wire_to_check)
        exit()
    new_wire_list = []
    for wire in wire_list:
        in1,in2,gate_type,out = wire
        if ('x00', 'y00', 'XOR') == (in1, in2, gate_type):
            assert out == 'z00', 'x00 XOR y00 should give z00!'
            new_wire = (in1,in2,gate_type,'z00')
        else:
            new_wire = (in1,in2,gate_type,out)

        new_wire_list.append(new_wire)

    print(new_wire_list)

if __name__ == '__main__':
    input_filename = 'z-24-01-input.txt'
    # input_filename = 'z-24-02-actual-example.txt'
    # input_list, wire_list = read_wires(input_filename)
    circuit = Circuit(input_filename)
    circuit.make_translation()
    # wire_list = sort_wire_list(wire_list)
    # print(wire_list)
    # make_translation(wire_list)
    # circuit = Circuit(input_filename)
    # print(circuit.find_x_y_wires())
    # print(circuit.check_xor())
