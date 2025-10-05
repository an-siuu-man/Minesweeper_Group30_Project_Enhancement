# Minesweeper_Group30_Project Enhancement
Welcome to our Minesweeper Enhancement GitHub page! This repository is for the enhanced version of the original Minesweeper game created by Group 30. Here, we have integrated an AI co-op mode that allows players to team up with an AI opponent of varying difficulty levels (Easy, Medium, Hard) to solve the Minesweeper puzzle together.

**Team Members - Group 29**
- Ansuman Sharma
- Achinth Ulagapperoli
- Jahnvi Maddila
- Vamsi Doddapaneni
- Taha Khalid

## Added Feature: AI co-op mode

Play Minesweeper together with the computer! In AI co-op mode, you and the AI take turns making moves on the same board. You can choose the AI's difficulty (Easy, Medium, Hard) and watch as it uses logic and pattern recognition to help solve the puzzle. After each move, control switches between you and the AI, making it a collaborative experience. This mode is great for learning strategies, testing AI logic, or just having fun with a smart teammate.

**How it works:**
- Enable AI mode on the front page and start the game.
- You and the AI alternate turns (flagging or revealing cells).
- The HUD shows whose turn it is.
- Choose AI difficulty: Easy (random), Medium (basic logic), Hard (advanced patterns).
- Win or lose together!

## AI Solver Overview

This project adds a rule-based AI solver to Minesweeper with three difficulty levels:

- **Easy:** AI clicks random hidden cells.
- **Medium:** AI uses basic logic:
  - Flags hidden neighbors if their count matches the cell’s number.
  - Clicks hidden neighbors if the number of flagged neighbors matches the cell’s number.
  - Falls back to random if no rule applies.
- **Hard:** AI uses all Medium rules plus the “1-2-1” pattern:
  - Recognizes three adjacent cells showing 1-2-1 and deduces which neighbors are mines or safe.

**How to use:**
- Enable AI mode and select difficulty on the front page.
- Play solo or co-op (alternate turns with the AI).
- The HUD shows whose turn it is and the AI’s difficulty.

**Technical notes:**
- All AI logic is in `ai_solver.py`.
- The AI is integrated into the game loop in `game.py`.
- The AI’s move speed is adjustable.
- The code is modular and easy to extend.

**Limitations:**
- No probability-based guessing.
- Only the 1-2-1 pattern is recognized for advanced logic.
- First move is always random.


## How to launch the game

1. Clone the repository:
```
  git clone https://github.com/an-siuu-man/Minesweeper_Group30_Project_Enhancement.git
```
2. Navigate to the project directory:
```
  cd Minesweeper_Group30_Project_Enhancement
```
3. (Optional) Create and activate a virtual environment:
```
  python -m venv .venv
  source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

4. Install required packages:
```
  pip install -r requirements.txt
```
5. Run the game:
```
  python main.py
```
6. Enjoy playing Minesweeper with AI co-op mode!
<br>
<br>

# Original README Content

How does Minesweeper work? In this game, you can select how many bombs you want to place on the board. They will be randomly placed on the board and hidden from the user. The user has to try to click on all the non-bomb cells to win. If they suspect a cell to be a bomb, they can flag it via right-click. As the user clicks on cells, they will get hints to how many bombs are adjacent to that cell they clicked on.
<br>
**Team Members - Group 30**
- Sophia Jacob
- Anna Lin
- Kusuma Murthy
- Nikka Vuong
- Nimra Syed

**Note:** Please visit our Wiki Page at the top to see our Meeting Logs.

**Links**:
- [Team Meeting Logs](https://github.com/SAJacob7/Minesweeper_Group30_Project/wiki/Team-Meeting-Logs)
- [Sprint Board 1](https://github.com/users/SAJacob7/projects/1)
- [Sprint Board 2](https://github.com/users/SAJacob7/projects/3)



## Project Deliverables (Documentation):
- Project System Architecture and Person-Hour Estimates: Contains our diagrams of our code flow, person-hour logs, and explanation of our code.
- Meeting Logs
- Sprint Boards + Tickets
## Project Deliverables (Code):
- cell.py
- grid.py
- game.py
- settings.py
- main.py: Use this file to run the code.
- Assets Folder (Contains all the drawings for the grid board, cells, front page, and more.)
## User Manual
Start by cloning this GitHub repo as seen below.
```
  git clone https://github.com/SAJacob7/Minesweeper_Group30_Project.git
```
After ensuring you have all the required modules and dependencies, run the main.py file by doing:
```
  python3 main.py
```
