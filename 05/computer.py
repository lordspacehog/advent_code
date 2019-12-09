from collections.abc import Iterator
from functools import partial
from typing import Callable, Tuple


class IntcodeComputer(Iterator):
    __pc: int = 0
    __instructions = {
        '01': (3, 'add'),
        '02': (3, 'mult'),
        '03': (1, 'input_'),
        '04': (1, 'output'),
        '05': (2, 'jnz'),
        '06': (2, 'jz'),
        '07': (3, 'lt'),
        '08': (3, 'eq'),
        '99': (0, 'halt'),
    }

    def __init__(self, program: str):
        self.__program = list(map(int, program.split(',')))

    def __iter__(self):
        return self

    def __next__(self):
        if self.__pc > len(self.__program):
            print(f'pc out of range! {self.__pc}')
            self.halt()

        encoded_opc = self.__program[self.__pc]

        param_cnt, inst = self.instruction(encoded_opc)

        if param_cnt == 0:
            inst()
            return

        params = self.__program[self.__pc+1:self.__pc+1+param_cnt]
        inst(*params)

    @staticmethod
    def parse_opcode(opc: int) -> (int, int, int, str):
        A, B, C, *DE = f'{opc:05d}'
        return tuple(map(int, (C, B, A))) + (''.join(DE),)

    def instruction(self, instruction: int) -> (int, Callable[..., None]):
        decoded_instruction = self.parse_opcode(instruction)
        instruction_proto = self.__instructions[decoded_instruction[3]]

        if instruction_proto[0] == 3:
            return (
                instruction_proto[0],
                partial(
                    getattr(self, instruction_proto[1]),
                    decoded_instruction[:3]
                )
            )

        if instruction_proto[0] == 2:
            return (
                instruction_proto[0],
                partial(
                    getattr(self, instruction_proto[1]),
                    decoded_instruction[:2]
                )
            )

        if instruction_proto[0] == 1:
            return (
                instruction_proto[0],
                partial(
                    getattr(self, instruction_proto[1]),
                    decoded_instruction[0]
                )
            )

        return (0, getattr(self, instruction_proto[1]))

    def add(self, modes: Tuple[int, int, int],
            opr1: int, opr2: int, opr3: int) -> None:
        opr1_mode, opr2_mode, opr3_mode = modes

        val1 = self.get_param_value(opr1_mode, opr1)
        val2 = self.get_param_value(opr2_mode, opr2)

        self.__program[opr3] = val1 + val2
        self.__pc += 4

    def mult(self, modes: Tuple[int, int, int],
             opr1: int, opr2: int, opr3: int) -> None:
        opr1_mode, opr2_mode, opr3_mode = modes

        val1 = self.get_param_value(opr1_mode, opr1)
        val2 = self.get_param_value(opr2_mode, opr2)

        self.__program[opr3] = val1 * val2
        self.__pc += 4

    def jnz(self, modes: Tuple[int, int],
            opr1: int, opr2: int) -> None:
        opr1_mode, opr2_mode = modes

        val1 = self.get_param_value(opr1_mode, opr1)
        val2 = self.get_param_value(opr2_mode, opr2)

        if val1:
            self.__pc = val2
            return

        self.__pc += 3

    def jz(self, modes: Tuple[int, int],
            opr1: int, opr2: int) -> None:
        opr1_mode, opr2_mode = modes

        val1 = self.get_param_value(opr1_mode, opr1)
        val2 = self.get_param_value(opr2_mode, opr2)

        if not val1:
            self.__pc = val2
            return

        self.__pc += 3

    def lt(self, modes: Tuple[int, int, int],
            opr1: int, opr2: int, opr3: int) -> None:
        opr1_mode, opr2_mode, opr3_mode = modes

        val1 = self.get_param_value(opr1_mode, opr1)
        val2 = self.get_param_value(opr2_mode, opr2)

        if val1 < val2:
            self.__program[opr3] = 1
        else:
            self.__program[opr3] = 0

        self.__pc += 4

    def eq(self, modes: Tuple[int, int, int],
            opr1: int, opr2: int, opr3: int) -> None:
        opr1_mode, opr2_mode, opr3_mode = modes

        val1 = self.get_param_value(opr1_mode, opr1)
        val2 = self.get_param_value(opr2_mode, opr2)

        if val1 == val2:
            self.__program[opr3] = 1
        else:
            self.__program[opr3] = 0

        self.__pc += 4

    def input_(self, mode: int, opr: int) -> None:

        while True:
            in_val = input("input: ").rstrip()
            if not in_val.isnumeric():
                print("Invalid Input, must be numeric")
                continue
            in_val = int(in_val)
            break

        self.__program[opr] = in_val
        self.__pc += 2

    def output(self, mode: int, opr: int) -> None:
        val = self.get_param_value(mode, opr)
        print(f'output: {val:d}')
        self.__pc += 2

    def halt(self):
        print(f'final: {self.__program[0]}')
        raise StopIteration

    def get_param_value(self, mode: int, opr: int) -> int:
        if mode == 0:
            return self.__program[opr]

        if mode == 1:
            return opr

        raise RuntimeError("invalid addressing mode")

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
