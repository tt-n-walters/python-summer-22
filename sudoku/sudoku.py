import random

class Sudoku:
    def __init__(self):
        self.attempts = 0
    
    @classmethod
    def choose(cls, index):
        lines = Sudoku.read_puzzle_file()
        puzzle_string = lines[index]
        sudoku = cls()
        sudoku.parse_puzzle_string(puzzle_string)
        return sudoku


    @classmethod
    def random(cls):
        lines = Sudoku.read_puzzle_file()
        puzzle_string = random.choice(lines)
        sudoku = cls()
        sudoku.parse_puzzle_string(puzzle_string)
        return sudoku


    @classmethod
    def read_puzzle_file(cls):
        filename = "sudoku/puzzles.dat"
        file = open(filename, "r")
        contents = file.read()

        lines = contents.splitlines()
        return lines


    def parse_puzzle_string(self, puzzle_string):
        digits = list(puzzle_string)

        for i in range(81):
            digits[i] = int(digits[i])

        puzzle = []
        for i in range(9):
            row = digits[i * 9 : i * 9 + 9]
            puzzle.append(row)
        # return puzzle
        self.puzzle = puzzle


    def __repr__(self):
        buffer = ""
        buffer += "┏━━━━━━━┯━━━━━━━┯━━━━━━━┓" + "\n"
        for i in range(9):      # row
            row = []
            for j in range(9):  # column
                digit = self.puzzle[i][j]
                if digit > 0:
                    row.append(str(digit))
                else:
                    row.append(" ")
                
                if (j + 1) % 3  == 0 and j < 8:
                    row.append("│")

            row_string = " ".join(row)
            buffer += "┃ " + row_string + " ┃" + "\n"

            if (i + 1) % 3 == 0 and i < 8:
                buffer += "┠───────┼───────┼───────┨" + "\n"
            
        buffer += "┗━━━━━━━┷━━━━━━━┷━━━━━━━┛" + "\n"
        return buffer


    def check_position(self, column, row, number):
        # Check if __number__ can be placed in puzzle[__row__][__column__]

        # check row
        if number in self.puzzle[row]:
            return False
        
        # check column
        for i in range(9):
            if number == self.puzzle[i][column]:
                return False

        # check section
        section_x = column // 3 * 3
        section_y = row // 3 * 3
        for i in range(3):
            for j in range(3):
                if number == self.puzzle[section_y + i][section_x + j]:
                    return False
        
        return True


    # heuristic recursive backtracking algorithm
    # 1. Find an empty position
    # 2. Check numbers 1-10, find one that could fit. Place in the puzzle
    # 3. Repeat until steps 1 and 2 until either:
    #       - Puzzle is completely filled, solved.
    #       - A position with no possible numbers is found.
    #         If so, remove the previous guess, start from step 1.

    def solve(self):
        self.attempts += 1
        for row in range(9):            # Find the next empty position
            for column in range(9):
                number = self.puzzle[row][column]
                if number == 0:

                    for n in range(1, 10):        # Check every number 1-9 if they fit
                        if self.check_position(column, row, n):
                            self.puzzle[row][column] = n

                            yield from self.solve()

                            self.puzzle[row][column] = 0
                    
                    # Here's where the was a mistake. No numbers 1-10 fit
                    return

        print(self, file=file)
        yield


if __name__ == "__main__":
    sudoku = Sudoku.choose(1)
    print("Solving random sudoku...")
    file = open("puzzle_output.txt", "w", encoding="utf-8")
    print(sudoku, file=file)
    solver = sudoku.solve()
    for _ in solver:
        if sudoku.attempts % 127 == 0:
            print(f"  {sudoku.attempts} attempts...", end="     \r")
    print()
    