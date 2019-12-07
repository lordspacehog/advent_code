from collections.abc import Iterator
from functools import partial
from typing import Callable, Tuple, List


class InstructionSet(object):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(InstructionSet, cls).__new__(cls)
        return cls.__instance

    def __setattr__(cls, name, value):
        raise AttributeError("Attributes for this class are immutable")

    def __delattr__(cls, name, value):
        raise AttributeError("Attributes for this class are immutable")


class IntcodeComputer(Iterator):
    __pc: int = 0
    __instructions = {
        '01': (3, 'add'),
        '02': (3, 'mult'),
        '03': (1, 'input_'),
        '04': (1, 'output'),
        '99': (0, 'halt'),
    }

    def __init__(self, program: str):
        self.__program = list(map(int, program.split(',')))

    def __iter__(self):
        return self

    def __next__(self):
        if not self.__pc < len(self.__program):
            self.__halt()

        encoded_opc = self.__program[self.__pc]

        param_cnt, inst = self.__instr.instruction(encoded_opc)

        if param_cnt == 0:
            inst(self.__program)
            return

        params = self.__program[self.__pc+1:self.__pc+1+param_cnt]
        inst(*params, self.__program)

        self.__pc += (param_cnt + 1)

        return

    def instruction(self, instruction: int) -> (int, Callable[..., None]):
        decoded_instruction = self.parse_opcode(instruction)
        instruction_proto = self.__instructions[decoded_instruction[3]]

        if instruction_proto[0] == 3:
            return (
                instruction_proto[0],
                partial(
                    getattr(InstructionSet, instruction_proto[1]),
                    decoded_instruction[:3]
                )
            )

        if instruction_proto[0] == 2:
            return (
                instruction_proto[0],
                partial(
                    getattr(InstructionSet, instruction_proto[1]),
                    decoded_instruction[1:3]
                )
            )

        if instruction_proto[0] == 1:
            return (
                instruction_proto[0],
                partial(
                    getattr(InstructionSet, instruction_proto[1]),
                    decoded_instruction[2]
                )
            )

        return (0, getattr(InstructionSet, instruction_proto[1]))

    @staticmethod
    def add(
        modes: Tuple[int, int, int],
        opr1: int, opr2: int, opr3: int, memory: List[int]
    ) -> None:
        opr1_mode, opr2_mode, opr3_mode = modes

        val1 = InstructionSet.get_param_value(opr1_mode, opr1, memory)
        val2 = InstructionSet.get_param_value(opr2_mode, opr2, memory)

        memory[opr3] = val1 + val2

    @staticmethod
    def mult(
        modes: Tuple[int, int, int],
        opr1: int, opr2: int, opr3: int, memory: List[int]
    ) -> None:
        opr1_mode, opr2_mode, opr3_mode = modes

        val1 = InstructionSet.get_param_value(opr1_mode, opr1, memory)
        val2 = InstructionSet.get_param_value(opr2_mode, opr2, memory)

        memory[opr3] = val1 * val2
        return

    @staticmethod
    def input_(mode: int, opr: int, memory: List[int]) -> None:

        while True:
            in_val = input("input: ").rstrip()
            if not in_val.isnumeric():
                print("Invalid Input, must be numeric")
                continue
            in_val = int(in_val)
            break

        memory[opr] = in_val
        return

    @staticmethod
    def output(mode: int, opr: int, memory) -> None:
        val = InstructionSet.get_param_value(mode, opr, memory)
        print(f'output: {val:d}')

    @staticmethod
    def halt(memory):
        print(f'final: {memory[0]}')
        raise StopIteration

    @staticmethod
    def get_param_value(mode: int, opr: int, memory: List[int]) -> int:
        if mode == 0:
            return memory[opr]

        if mode == 1:
            return opr

        raise RuntimeError("invalid addressing mode")

    @staticmethod
    def parse_opcode(opc: int) -> (int, int, int, str):
        A, B, C, *DE = f'{opc:05d}'
        return tuple(map(int, (C, B, A))) + (''.join(DE),)
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
