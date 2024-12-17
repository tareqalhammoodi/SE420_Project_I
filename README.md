## AI Project1 2024-2025

You will implement a 3x3 board game. The aim is reaching the goal state where Tile #1, #2, and #3 are located on the board.

<table>
<tr>
<td>

### Requirements

1. The **initial and goal states** will be given by the user.
2. The tiles can be moved **up, down, right, or left**.
3. The game will begin by the move of **Tile #1** (if required) and go on with the moves of other tiles in order:  
    &nbsp;&nbsp;&nbsp;1st step: move Tile #1  
    &nbsp;&nbsp;&nbsp;2nd step: move Tile #2  
    &nbsp;&nbsp;&nbsp;3rd step: move Tile #3  
    &nbsp;&nbsp;&nbsp;4th step: move Tile #1  
    &nbsp;&nbsp;&nbsp;5th step: move Tile #2  
    &nbsp;&nbsp;&nbsp;6th step: move Tile #3  
    &nbsp;&nbsp;&nbsp;and so on ......  

4. The **distance (cost)** between two neighboring states will be measured based on the move costs:  
   &nbsp;&nbsp;&nbsp;Right or left move → cost = 2  
   &nbsp;&nbsp;&nbsp;Up or down move → cost = 1  

5. The **A*** search will be implemented with **Manhattan distance** as heuristics.
6. The expansion will go on till the **10th expanded node**. The program will **print out each expanded state** and compare it with the given goal state.

You are free to use any programming language for implementation.

</td>
<td>

<img src="https://github.com/user-attachments/assets/a65a7b79-4397-4755-bc09-b1ccea425a1c" width="600"/>

</td>
</tr>
</table>
