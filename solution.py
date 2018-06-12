
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[r+c for r, c in zip(rows, cols)], [r+c for r, c in zip(rows, cols[::-1])]]
unitlist = row_units + column_units + square_units + diagonal_units

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """

    def find_matches(box):
        matches = [box]
        value = sorted(values[box]) #values[box]
        for _box in unit:
            if box != _box:
                # This is a different box
                cur_val = sorted(values[_box]) #values[_box] # Value corresponding to current value
                if sorted(value) == sorted(cur_val):
                    # A match is found
                    matches.append(_box)
        return matches

    #unitlist = [['A1','A2','A3','A4','A5','A6','A7','A8','A9']]
    #print(unitlist)
    for unit in unitlist:
        naked_twins = {} # {twin_value: [box1, box2]}
        #print(unit)
        for box in unit:
            cur_val = ''.join(sorted(values[box])) #values[box]
            if len(cur_val) == 2:
                # It could be a twin
                matches = find_matches(box)
                if len(matches) == 2:
                    # It's a naked_twin, since there's only one match
                    naked_twins[cur_val] = sorted(matches)
        #print(naked_twins)
        for twin_value, twin_boxes in naked_twins.items():
            # Eliminate twin values from boxes in unit
            for box in unit:
                if box not in twin_boxes:
                    for v in twin_value:
                        values = assign_value(values, box, values[box].replace(v, ''))
    return values

def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """

    # Assemble a list of boxes with single values
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            # Remove digit from peers of this box
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        # Iterate over every unit
        for digit in '123456789':
            # Assemble a list of boxes containing this digit
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                # Only one box contains this digit
                values = assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    values = reduce_puzzle(values)
    # Choose one of the unfilled squares with the fewest possibilities
    if values is False:
        return False
    if all(len(values[i])==1 for i in boxes):
        return values
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    n,s = min((len(values[s]),s) for s in boxes if len(values[s])>1)

    for value in values[s]:
        new_sudoku=values.copy()
        new_sudoku[s]=value
        result=search(new_sudoku)
        if result:
            return result


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.

        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #diag_sudoku_grid = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
    #diag_sudoku_grid = '.......41......89...7....3........8.....47..2.......6.7.2........1.....4..6.9.3..'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
