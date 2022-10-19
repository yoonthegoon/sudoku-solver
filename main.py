import requests
from bs4 import BeautifulSoup


def scrape(url: str) -> list[list[int]]:
    url = url.replace('www', 'nine')  # frame source

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    grid = [[0 for _ in range(9)] for _ in range(9)]
    for y in range(9):
        for x in range(9):
            grid[y][x] = int(soup.find(id=f'f{x}{y}').get('value', '0'))

    return grid


def verify_row(grid: list[list[int]], y: int, guess: int) -> bool:
    if guess in grid[y]:
        return False
    return True


def verify_col(grid: list[list[int]], x: int, guess: int) -> bool:
    col = [row[x] for row in grid]
    if guess in col:
        return False
    return True


def verify_box(grid: list[list[int]], x: int, y: int, guess: int) -> bool:
    box = [grid[y // 3 * 3 + i // 3][x // 3 * 3 + i % 3] for i in range(9)]
    if guess in box:
        return False
    return True


def verify_pos(grid: list[list[int]], x: int, y: int, guess: int) -> bool:
    row = verify_row(grid, y, guess)
    col = verify_col(grid, x, guess)
    box = verify_box(grid, x, y, guess)
    return all((row, col, box))


def solve(grid: list[list[int]]) -> list[list[int]] or None:
    for y, row in enumerate(grid):
        for x, digit in enumerate(row):
            if not digit:
                for i in range(1, 10):
                    valid = verify_pos(grid, x, y, i)
                    if valid:
                        grid[y][x] = i
                        solution = solve(grid)

                        if solution:
                            return solution

                grid[y][x] = 0
                return

    return grid


def display(grid: list[list[int]]) -> None:
    for y, row in enumerate(grid):
        if y % 3 == 0:
            print('+-------+-------+-------+')

        for x, digit in enumerate(row):
            if x % 3 == 0:
                print('| ', end='')

            print(digit, end=' ') if digit else print('_', end=' ')

        print('|')

    print('+-------+-------+-------+\n')


def main(url: str):
    grid = scrape(url)
    solve(grid)
    display(grid)


if __name__ == '__main__':
    main('https://www.websudoku.com/?level=4&set_id=6001986830')
