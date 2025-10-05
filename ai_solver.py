# ai_solver.py
import random
from settings import ROWS, COLUMNS

class AISolver:
    def __init__(self, difficulty="easy"):
        """
        Initialize the AI solver with a specified difficulty level.
        
        Args:
            difficulty (str): One of "easy", "medium", or "hard"
        """
        self.difficulty = difficulty.lower()
        
    def get_move(self, grid):
        """
        Get the next move based on the current difficulty level.
        
        Args:
            grid: The Grid object containing the game state
            
        Returns:
            tuple: (action, row, col) where action is "click" or "flag"
                   Returns None if no valid move is available
        """
        if self.difficulty == "easy":
            return self.easy_move(grid)
        elif self.difficulty == "medium":
            return self.medium_move(grid)
        elif self.difficulty == "hard":
            return self.hard_move(grid)
        else:
            return self.easy_move(grid)
    
    def easy_move(self, grid):
        """
        Easy difficulty: Click on any random hidden cell.
        
        Args:
            grid: The Grid object containing the game state
            
        Returns:
            tuple: ("click", row, col) for a random unrevealed, unflagged cell
        """
        hidden_cells = []
        
        # Find all hidden cells that are not flagged
        for row in range(ROWS):
            for col in range(COLUMNS):
                cell = grid.grid_list[row][col]
                if not cell.revealed and not cell.flagged:
                    hidden_cells.append((row, col))
        
        if hidden_cells:
            row, col = random.choice(hidden_cells)
            return ("click", row, col)
        
        return None
    
    def medium_move(self, grid):
        """
        Medium difficulty: Apply basic Minesweeper logic rules.
        
        Rule 1: If a numbered cell has as many hidden neighbors as its number,
                flag all hidden neighbors as mines.
        Rule 2: If a numbered cell has as many flagged neighbors as its number,
                open all other hidden neighbors (they must be safe).
        
        Falls back to random move if no rules apply.
        
        Args:
            grid: The Grid object containing the game state
            
        Returns:
            tuple: ("click", row, col) or ("flag", row, col)
        """
        # First, try to apply Rule 1 (flag all hidden neighbors)
        move = self._apply_flag_rule(grid)
        if move:
            return move
        
        # Next, try to apply Rule 2 (click safe cells)
        move = self._apply_safe_click_rule(grid)
        if move:
            return move
        
        # If no rules apply, fall back to random move
        return self.easy_move(grid)
    
    def hard_move(self, grid):
        """
        Hard difficulty: Apply all medium rules plus the 1-2-1 pattern rule.
        
        1-2-1 Pattern Rule: If three adjacent revealed cells in a line show "1-2-1",
        the two outer hidden neighbors (perpendicular to the line) are mines,
        and the inner hidden neighbor is safe.
        
        Falls back to medium logic if pattern not found.
        
        Args:
            grid: The Grid object containing the game state
            
        Returns:
            tuple: ("click", row, col) or ("flag", row, col)
        """
        # First, try the 1-2-1 pattern rule
        move = self._apply_121_pattern_rule(grid)
        if move:
            return move
        
        # Fall back to medium difficulty logic
        return self.medium_move(grid)
    
    def _get_neighbors(self, row, col):
        """
        Get all valid neighbor coordinates for a given cell.
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            list: List of (row, col) tuples for valid neighbors
        """
        neighbors = []
        for row_offset in range(-1, 2):
            for col_offset in range(-1, 2):
                if row_offset == 0 and col_offset == 0:
                    continue
                    
                new_row = row + row_offset
                new_col = col + col_offset
                
                if 0 <= new_row < ROWS and 0 <= new_col < COLUMNS:
                    neighbors.append((new_row, new_col))
        
        return neighbors
    
    def _get_cell_number(self, cell):
        """
        Extract the number from a numbered cell.
        
        Args:
            cell: Cell object
            
        Returns:
            int: The number of adjacent mines (0-8), or None if not a numbered cell
        """
        if cell.type != "N":
            return None
        
        # Count adjacent bombs to determine the cell's number
        # This is a helper that recomputes it from the image list index
        from settings import cell_num_1, cell_num_2
        
        for i, img in enumerate(cell_num_1):
            if cell.image == img:
                return i + 1
        
        for i, img in enumerate(cell_num_2):
            if cell.image == img:
                return i + 1
        
        return None
    
    def _apply_flag_rule(self, grid):
        """
        Rule 1: If number of hidden neighbors equals the cell's number, flag them all.
        
        Args:
            grid: The Grid object
            
        Returns:
            tuple: ("flag", row, col) or None
        """
        for row in range(ROWS):
            for col in range(COLUMNS):
                cell = grid.grid_list[row][col]
                
                # Only process revealed numbered cells
                if not cell.revealed or cell.type != "N":
                    continue
                
                cell_number = self._get_cell_number(cell)
                if cell_number is None:
                    continue
                
                neighbors = self._get_neighbors(row, col)
                hidden_neighbors = []
                flagged_count = 0
                
                for n_row, n_col in neighbors:
                    n_cell = grid.grid_list[n_row][n_col]
                    if n_cell.flagged:
                        flagged_count += 1
                    elif not n_cell.revealed:
                        hidden_neighbors.append((n_row, n_col))
                
                # If hidden + flagged count equals cell number, flag all hidden
                if len(hidden_neighbors) + flagged_count == cell_number and hidden_neighbors:
                    flag_row, flag_col = hidden_neighbors[0]
                    return ("flag", flag_row, flag_col)
        
        return None
    
    def _apply_safe_click_rule(self, grid):
        """
        Rule 2: If flagged neighbors equals the cell's number, click all hidden neighbors.
        
        Args:
            grid: The Grid object
            
        Returns:
            tuple: ("click", row, col) or None
        """
        for row in range(ROWS):
            for col in range(COLUMNS):
                cell = grid.grid_list[row][col]
                
                # Only process revealed numbered cells
                if not cell.revealed or cell.type != "N":
                    continue
                
                cell_number = self._get_cell_number(cell)
                if cell_number is None:
                    continue
                
                neighbors = self._get_neighbors(row, col)
                hidden_neighbors = []
                flagged_count = 0
                
                for n_row, n_col in neighbors:
                    n_cell = grid.grid_list[n_row][n_col]
                    if n_cell.flagged:
                        flagged_count += 1
                    elif not n_cell.revealed:
                        hidden_neighbors.append((n_row, n_col))
                
                # If flagged count equals cell number, all hidden neighbors are safe
                if flagged_count == cell_number and hidden_neighbors:
                    click_row, click_col = hidden_neighbors[0]
                    return ("click", click_row, click_col)
        
        return None
    
    def _apply_121_pattern_rule(self, grid):
        """
        1-2-1 Pattern Rule: Detect and act on 1-2-1 patterns in horizontal or vertical lines.
        
        Pattern: If three adjacent cells in a line show 1-2-1:
        - The two cells perpendicular to the outer 1's (on opposite sides) are mines
        - The cells perpendicular to the center 2 are safe
        
        Args:
            grid: The Grid object
            
        Returns:
            tuple: ("flag", row, col) or ("click", row, col) or None
        """
        # Check horizontal 1-2-1 patterns
        for row in range(ROWS):
            for col in range(COLUMNS - 2):
                cell1 = grid.grid_list[row][col]
                cell2 = grid.grid_list[row][col + 1]
                cell3 = grid.grid_list[row][col + 2]
                
                if (cell1.revealed and cell2.revealed and cell3.revealed and
                    cell1.type == "N" and cell2.type == "N" and cell3.type == "N"):
                    
                    num1 = self._get_cell_number(cell1)
                    num2 = self._get_cell_number(cell2)
                    num3 = self._get_cell_number(cell3)
                    
                    if num1 == 1 and num2 == 2 and num3 == 1:
                        # Found horizontal 1-2-1 pattern
                        move = self._handle_horizontal_121(grid, row, col)
                        if move:
                            return move
        
        # Check vertical 1-2-1 patterns
        for row in range(ROWS - 2):
            for col in range(COLUMNS):
                cell1 = grid.grid_list[row][col]
                cell2 = grid.grid_list[row + 1][col]
                cell3 = grid.grid_list[row + 2][col]
                
                if (cell1.revealed and cell2.revealed and cell3.revealed and
                    cell1.type == "N" and cell2.type == "N" and cell3.type == "N"):
                    
                    num1 = self._get_cell_number(cell1)
                    num2 = self._get_cell_number(cell2)
                    num3 = self._get_cell_number(cell3)
                    
                    if num1 == 1 and num2 == 2 and num3 == 1:
                        # Found vertical 1-2-1 pattern
                        move = self._handle_vertical_121(grid, row, col)
                        if move:
                            return move
        
        return None
    
    def _handle_horizontal_121(self, grid, row, col):
        """
        Handle a horizontal 1-2-1 pattern at position (row, col).
        
        The pattern is at cells: (row, col), (row, col+1), (row, col+2)
        Mines are typically at cells above/below the outer 1's.
        Safe cells are typically above/below the center 2.
        
        Args:
            grid: The Grid object
            row (int): Row of the first '1' in the pattern
            col (int): Column of the first '1' in the pattern
            
        Returns:
            tuple: ("flag", r, c) or ("click", r, c) or None
        """
        # Check cells above and below each position
        # For outer 1's, perpendicular cells are likely mines
        # For center 2, perpendicular cells are likely safe
        
        # Check above and below the first 1
        for r_offset in [-1, 1]:
            new_row = row + r_offset
            if 0 <= new_row < ROWS:
                cell = grid.grid_list[new_row][col]
                if not cell.revealed and not cell.flagged:
                    # This should be a mine
                    return ("flag", new_row, col)
        
        # Check above and below the center 2
        for r_offset in [-1, 1]:
            new_row = row + r_offset
            if 0 <= new_row < ROWS:
                cell = grid.grid_list[new_row][col + 1]
                if not cell.revealed and not cell.flagged:
                    # This should be safe
                    return ("click", new_row, col + 1)
        
        # Check above and below the last 1
        for r_offset in [-1, 1]:
            new_row = row + r_offset
            if 0 <= new_row < ROWS:
                cell = grid.grid_list[new_row][col + 2]
                if not cell.revealed and not cell.flagged:
                    # This should be a mine
                    return ("flag", new_row, col + 2)
        
        return None
    
    def _handle_vertical_121(self, grid, row, col):
        """
        Handle a vertical 1-2-1 pattern at position (row, col).
        
        The pattern is at cells: (row, col), (row+1, col), (row+2, col)
        Mines are typically at cells left/right of the outer 1's.
        Safe cells are typically left/right of the center 2.
        
        Args:
            grid: The Grid object
            row (int): Row of the first '1' in the pattern
            col (int): Column of the first '1' in the pattern
            
        Returns:
            tuple: ("flag", r, c) or ("click", r, c) or None
        """
        # Check cells left and right of each position
        # For outer 1's, perpendicular cells are likely mines
        # For center 2, perpendicular cells are likely safe
        
        # Check left and right of the first 1
        for c_offset in [-1, 1]:
            new_col = col + c_offset
            if 0 <= new_col < COLUMNS:
                cell = grid.grid_list[row][new_col]
                if not cell.revealed and not cell.flagged:
                    # This should be a mine
                    return ("flag", row, new_col)
        
        # Check left and right of the center 2
        for c_offset in [-1, 1]:
            new_col = col + c_offset
            if 0 <= new_col < COLUMNS:
                cell = grid.grid_list[row + 1][new_col]
                if not cell.revealed and not cell.flagged:
                    # This should be safe
                    return ("click", row + 1, new_col)
        
        # Check left and right of the last 1
        for c_offset in [-1, 1]:
            new_col = col + c_offset
            if 0 <= new_col < COLUMNS:
                cell = grid.grid_list[row + 2][new_col]
                if not cell.revealed and not cell.flagged:
                    # This should be a mine
                    return ("flag", row + 2, new_col)
        
        return None
