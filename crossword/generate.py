import collections
import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable, values in self.domains.items():
            for value in values.copy():
                # If a value doesn't satisfy the length unary constraint,
                # it'll be removed from the variable domain.
                if len(value) != variable.length:
                    self.domains[variable].remove(value)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlaps = self.overlaps()

        for value_x in self.domains[x].copy():
            # We find the indexes for the overlapping characters' positions.
            x_index = overlaps[x, y][0]
            y_index = overlaps[x, y][1]
            matches = 0

            for value_y in self.domains[y]:
                # If the characters in the overlapping positions given by the indexes match,
                # we increase the matches by 1.
                if value_x[x_index] == value_y[y_index]:
                    matches += 1
            # If there are no matches at all for that value_x in y domain,
            # we remove the value from x domain and we set revised to true.
            if matches == 0:
                self.domains[x].remove(value_x)
                revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # We set the queue to the arcs if arcs is passed,
        # otherwise we set it to a list of all overlaps.
        queue = arcs if arcs is not None else list(self.overlaps())

        while len(queue) != 0:
            # Until the queue is not empty, we keep extracting a pair of
            # variables from it.
            x, y = queue.pop()

            if self.revise(x, y):
                # If, after revising the pair, the domain of x is empty, we return False
                if len(self.domains[x]) == 0:
                    return False
                # We add to the queue all the pairs made by x and its neighbours,
                # except for the one already examined.
                for nb in self.crossword.neighbors(x) - {y}:
                    queue.append((nb, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Returns True if all the assignment keys match the variables and
        # the values are not None or empty strings.
        completed = (self.crossword.variables == assignment.keys() and all(assignment.values()))

        return completed

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        overlaps = self.overlaps()
        var_occurrences = dict(collections.Counter(assignment.values()))
        no_conflicts = list()
        # Checks if any of the assigned values' length is different from the variable's length.
        if any(len(assignment[var]) != var.length for var in assignment):
            return False
        # Checks for values that have been assigned more than once.
        if any(occ > 1 for occ in var_occurrences.values()):
            return False

        for var in assignment:
            for nb in self.crossword.neighbors(var):
                if nb in assignment:
                    var_index = overlaps[var, nb][0]
                    nb_index = overlaps[var, nb][1]
                    # Checks for conflicting overlapping values.
                    if assignment[var][var_index] == assignment[nb][nb_index]:
                        no_conflicts.append(True)
                    else:
                        no_conflicts.append(False)
        # Returns false if there are conflicts.
        if not all(no_conflicts):
            return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        unassigned_vars = self.crossword.neighbors(var) - set(assignment.keys())

        overlaps = self.overlaps()

        ruled_out_values = dict()
        # For each value in the variable domain,
        for value_x in self.domains[var]:
            ruled_out_values_count = 0
            # we find the unassigned neighbouring variables and their overlapping values.
            for un_var in unassigned_vars:
                x_index = overlaps[var, un_var][0]
                y_index = overlaps[var, un_var][1]

                for value_y in self.domains[un_var]:
                    # If the characters in the overlapping positions given by the indexes don't match,
                    # we increase the ruled_out_values_count by 1.
                    if value_x[x_index] != value_y[y_index]:
                        ruled_out_values_count += 1
            # Finally, we assign to each value its corresponding ruled_out_values_count
            ruled_out_values[value_x] = ruled_out_values_count
        # and we sort the value in ascending order (using the sort() method defined below).
        sorted_values = sort(ruled_out_values)

        return sorted_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        variables = self.crossword.variables - set(assignment.keys())
        # We assign to each remaining variable the count of the values still in its domain.
        mrvs = {var: len(self.domains[var]) for var in variables}
        # We find the minimum value between all the variables' values count.
        min_value = min(mrvs.values())
        # We find the one (or ones) whose value correspond to the min value.
        mrv_vars = list(filter(lambda x: mrvs[x] == min_value, mrvs))
        # If there's only one variable in the resulting list, we return it,
        # otherwise we assign to each variable's neighbour in mrv_vars the count of the values in its domain,
        # we find the maximum value between all the neighbour' values count,
        # and we find the one (or ones) whose value correspond to the max value.
        # If it's still a tie, we just return the first one.
        # (as "any of the tied variables are acceptable return values").
        if len(mrv_vars) == 1:
            variable = mrv_vars[0]
        else:
            degrees = {var: len(self.crossword.neighbors(var)) for var in mrv_vars}
            max_value = max(degrees.values())
            degree_vars = list(filter(lambda x: degrees[x] == max_value, degrees))
            variable = degree_vars[0]

        return variable

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        # Finds an unassigned variable.
        var = self.select_unassigned_variable(assignment)
        # Sets the arcs for the AC-3 function.
        arcs = [(neighbor, var) for neighbor in self.crossword.neighbors(var)]

        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            # For each value in the ordered domain values, we check overall consistency
            # and arc consistency after adding a variable to the assignment.
            if self.consistent(assignment):
                if self.ac3(arcs):
                    # If checks are successful, we recursively call the backtrack function,
                    result = self.backtrack(assignment)
                    # and if the result is not none, we return it (the completed assignment).
                    if result is not None:
                        return result

                    del assignment[var]

        return None

    # Removes all the overlaps pairs whose value is None.
    def overlaps(self):
        overlaps = {key: val for key, val in self.crossword.overlaps.items() if val is not None}

        return overlaps


# Returns a sorted dictionary.
def sort(dictionary):
    sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1]))

    return sorted_dict


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
