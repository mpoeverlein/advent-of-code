gate_types = {
        'AND': lambda a,b: a * b,
        'OR':  lambda a,b: max(a,b),
        'XOR': lambda a,b: (a+b) % 2,
    }

class Wire:
    def __init__(self, name: str, value: int) -> None:
        self.name = name
        self.value = value # 0 or 1 or -1 for no value
    def __repr__(self) -> str:
        return f'Wire: Name {self.name}, Value {self.value}'

class Gate:
    def __init__(self,
        in_wire1: Wire, in_wire2: Wire,
        out_wire: Wire, gate_type: str
        ) -> None:
        self.in1 = in_wire1
        self.in2 = in_wire2
        self.out = out_wire
        self.gate_type_name = gate_type
        self.gate_type = gate_types[gate_type]

    def apply(self) -> None:
        if self.in1.value == -1 or self.in2.value == -1:
            return -1
        print(self)
        self.out.value = self.gate_type(self.in1.value, self.in2.value)

    def __repr__(self) -> str:
        return f'Gate. In1: {self.in1.name} {self.in1.value}, In2: {self.in2.name} {self.in2.value}, Out: {self.out.name}, Type: {self.gate_type_name}'

class Circuit:
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

            wire_in1 = self.wire_dict.get(in1)
            wire_in2 = self.wire_dict.get(in2)
            wire_out = self.wire_dict.get(out)
            print(wire_in2)
            gate_list.append(Gate(wire_in1, wire_in2, wire_out, gate_type))

        self.gates = gate_list
        print(self.gates)
        print(self.wire_dict)
        # exit()

    def execute(self) -> None:
        while any([i.value == -1 for i in self.wire_dict.values()]):
            print(self.wire_dict.values())
            for gate in self.gates:
                gate.apply()

    def __repr__(self) -> None:
        result = ''
        for name, wire in self.wire_dict.items():
            result += f'Wire {name}, value {wire.value}\n'
        return result

    def get_secret_number(self, starting_string: str='z') -> int:
        self.wire_list = list(self.wire_dict.values())
        self.wire_list.sort(key=lambda wire: wire.name)
        secret_binary = ''
        for wire in self.wire_list:
            if not wire.name.startswith(starting_string): continue
            print(wire)
            secret_binary += str(wire.value)
        return int(secret_binary[::-1], 2)

if __name__ == '__main__':
    input_filename = 'z-24-01-input.txt'
    # input_filename = 'z-24-02-actual-example.txt'
    circuit = Circuit(input_filename)
    circuit.execute()
    print(circuit)
    print(circuit.get_secret_number())
