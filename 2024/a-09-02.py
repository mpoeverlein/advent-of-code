from copy import deepcopy
'''
represent both filled and empty blocks by DataBlock objects
empty blocks have negative id_values, starting at the left with -1
'''

class DataBlock:
    def __init__(self, id_value: int, start: int, length: int) -> None:
        self.id_value = id_value
        self.start = start
        self.length = length
    def __repr__(self) -> str:
        return f'DataBlock object. ID: {self.id_value}, start: {self.start}, length: {self.length}'

class Disk:
    def __init__(self, input_filename: str) -> None:
        with open(input_filename, 'r') as ff:
            line = ff.readline()
        datablocks = []
        filled, empty = 0, -1
        position = 0
        for c,value in enumerate(line.strip()):
            value = int(value)
            if c%2 == 0:
                datablocks.append(DataBlock(filled, position, value))
                position += value
                filled += 1
            else:
                datablocks.append(DataBlock(empty, position, value))
                position += value
                empty -= 1

        # self.datablocks = datablocks
        self.datablocks = {db.id_value: db for db in datablocks}

    def clean_up(self) -> bool:
        ''' remove zero length datablocks and merge adjacent empty blocks
        to indicate how long to clean up, a boolean is returned (true if two empty fields were merged)
        '''
        self.remove_zero_length_datablocks()
        self.datablocks = self.get_sorted_datablocks()
        datablocks = [db for k,db in self.datablocks.items()]
        datablocks.sort(key=lambda x: x.start)
        sorted_ids = [db.id_value for db in datablocks]
        for a,b in zip(sorted_ids, sorted_ids[1:]):
            if a < 0 and b < 0:
                self.set_length(a, self.get_length(a)+self.get_length(b))
                self.datablocks.pop(b)
                return True
        return False


    def remove_zero_length_datablocks(self) -> None:
        self.datablocks = {k: v for k,v in self.datablocks.items() if v.length > 0}

    def get_sorted_datablocks(self) -> dict[int, DataBlock]:
        datablocks = [db for k,db in self.datablocks.items()]
        datablocks.sort(key=lambda x: x.start)
        self.datablocks = {db.id_value: db for db in datablocks}
        return self.datablocks

    def __repr__(self) -> str:
        self.remove_zero_length_datablocks()
        result = ''
        for db in self.get_sorted_datablocks():
            if db.id_value < 0:
                result += db.length * '.'
            else:
                result += db.length * str(db.id_value)
        return result

    def get_start(self, id_value: int) -> int:
        return self.datablocks[id_value].start

    def get_length(self, id_value: int) -> int:
        return self.datablocks[id_value].length

    def set_start(self, id_value: int, new_start: int) -> None:
        self.datablocks[id_value].start = new_start

    def set_length(self, id_value: int, new_length: int) -> None:
        self.datablocks[id_value].length = new_length

    def move_block(self, move_id_value: int) -> bool:
        ''' returns boolean: True: the block was moved, False: the block was not moved '''
        print(move_id_value)
        assert move_id_value >= 0, 'Only filled blocks movable! (ID >= 0)'
        # self.remove_zero_length_datablocks()
        move_length = self.get_length(move_id_value)
        move_start = self.get_start(move_id_value)
        id_values = list(self.datablocks.keys())
        for target in range(-1, min(id_values)-1, -1):
            if target not in self.datablocks.keys(): continue
            target_start, target_length = self.get_start(target), self.get_length(target)
            if not(target in id_values \
                   and target_length >= move_length \
                   and target_start < move_start):
                continue

            # self.datablocks.append(DataBlock(min(id_values)-1, move_start, move_length))
            self.datablocks.update({min(id_values)-1: DataBlock(min(id_values)-1, move_start, move_length)})
            self.set_start(move_id_value, target_start)
            self.set_start(target, target_start + move_length)
            self.set_length(target, target_length - move_length)
            return True

        return False

    def compress(self) -> None:
        id_values = list(self.datablocks.keys())
        for i in range(max(id_values), -1, -1):
            block_was_moved = self.move_block(i)
            if block_was_moved:
                while self.clean_up():
                    pass

    def checksum(self) -> int:
        counter = 0
        for db in self.datablocks.values():
            if db.id_value < 0: continue
            for i in range(db.length):
                counter += db.id_value * (db.start + i)

        return counter


if __name__ == '__main__':
    # input_filename = 'z-09-02-actual-example.txt'
    input_filename = 'z-09-01-input.txt'
    disk = Disk(input_filename)
    print(disk.datablocks)
    # print(disk)
    # disk.move_block(9)
    disk.compress()
    # print(disk)
    print(disk.datablocks)
    print(disk.checksum())

