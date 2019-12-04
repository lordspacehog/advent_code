from collections.abc import Iterator


class GuidanceComputer(Iterator):
    __tape_position: int = 0

    def __init__(self, program: str):
        self.__program = list(map(int, program.split(',')))

    def __iter__(self):
        return self

    def __next__(self):
        if not self.__tape_position < len(self.__program):
            self.__halt()

        opc, opr1, opr2, opr3 = self.__program[slice(
            self.__tape_position,
            self.__tape_position+4
        )]

        if opc == 1:
            self.__program[opr3] = self.__program[opr1] + self.__program[opr2]
        elif opc == 2:
            self.__program[opr3] = self.__program[opr1] * self.__program[opr2]
        elif opc == 99:
            self.__halt()
        else:
            raise RuntimeError("got invalid opcode!")

        self.__tape_position += 4
        return

    def __halt(self):
        print(self.__program[0])
        raise StopIteration

    def get_memory_by_address(self, address: int):
        if not address < len(self.__program):
            raise RuntimeError("invalid memory location!")
        return self.__program[address]

    def update_memory_by_address(self, address: int, value: int):
        if not address < len(self.__program):
            raise RuntimeError("invalid memory location!")

        self.__program[address] = value

    def run(self):
        try:
            while True:
                next(self)
        except StopIteration:
            pass

        return
