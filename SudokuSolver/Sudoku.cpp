// Henry Bogardus

#include "Sudoku.h"
#include <iostream>
#include <fstream>
#include <string>
#include <stdlib.h>
#include <math.h>
using namespace std;

/*
 * constructor
 */
Sudoku::Sudoku() {
    puzzle = new int*[COLUMNS];
    for (int i = 0; i < ROWS; i++){
        puzzle[i] = new int[ROWS];
    }
    for (int j = 0; j < ROWS; j++){
        for (int k = 0; k < COLUMNS; k++){
            puzzle[j][k] = 0;
        }
    }
}

/*
 * Loads the sudoku puzzle from the file into the puzzle[][] variable
 */
void Sudoku::loadFromFile(string filename) {
    ifstream file (filename);
    if (file.is_open()) {
        for (int i = 0; i < ROWS; i++) {
            for (int j = 0; j < COLUMNS; j++) {
                file >> puzzle[i][j];
            }
        }
        file.close();
    }
}

/*
 * Gives over control to recursiveSolve(), which can keep track of the 
 * current row and column a little better
 */
bool Sudoku::solve() {
    if (boardFilled())
        return true;
    return recursiveSolve(0, 0);
}

/*
 * Prints Sudoku object
 */
void Sudoku::print() const {
    for (int i = 0; i < ROWS; i++) {
        if (i == 3 || i == 6) {
            cout << "------|-------|------" << endl;
        }
        for (int j = 0; j < COLUMNS; j++) {
            if (j == 3 || j == 6) {
                cout << "| ";
            }
            cout << puzzle[i][j] << " ";
        }
        cout << endl;
    }
}

/*
 * Tests if the received Sudoku object is equal to the current Sudoku object
 */
bool Sudoku::equals(const Sudoku &other) const {
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLUMNS; j++) {
            if (puzzle[i][j] != other.puzzle[i][j])
                return false;
        }
    }
    return true;
}

/*
 * This is the recursive solve method that can keep track of the current row
 * and column numbers.
 */
bool Sudoku::recursiveSolve(int cRow, int cColumn) {
    if (puzzle[cRow][cColumn]==0) {
        for (int i = 1; i<=ROWS; i++) {
            if (ableToPlant(i, cRow, cColumn)) {
                puzzle[cRow][cColumn] = i;
                if (cColumn == COLUMNS-1) {
                    if (cRow == ROWS-1)
                        return true;
                    if (recursiveSolve(cRow+1, 0))
                        return true;
                } else {
                    if (recursiveSolve(cRow, cColumn+1))
                        return true;
                }
            }
            puzzle[cRow][cColumn] = 0;
        }
    } else {
        if (cColumn == COLUMNS-1) {
            if (cRow == ROWS-1) {
                return true;
            } else {
                if (recursiveSolve(cRow+1, 0))
                    return true;
            }
        } else {
            if (recursiveSolve(cRow, cColumn+1))
                return true;
        }
    }
    return false;
}

/*
 * Method runs through the puzzle 2d array and checks if there are any empty
 * spaces left, and if there are returns false.
 */
bool Sudoku::boardFilled() const {
    for (int i = 0; i < COLUMNS; i++) {
        for (int j = 0; j < ROWS; j++) {
            if (puzzle[i][j] == 0)
                return false;
        }
    }
    return true;
}

/*
 * Method accepts the current number the program is attempting to plant,
 * the current row and the current row and checks within the row if
 * the current number is already present
 */
bool Sudoku::numInRow(int cur, int cRow) const {
    for (int i = 0; i < COLUMNS; i++){
        if (puzzle[cRow][i] == cur)
            return true;
    }
    return false;
}

/*
 * Method accepts the current number the program is attempting to plant,
 * the current row and the current column and checks within the column if
 * the current number is already present
 */
bool Sudoku::numInColumn(int cur, int cColumn) const {
    for (int i = 0; i < ROWS; i++){
        if (puzzle[i][cColumn] == cur)
            return true;
    }
    return false;
}

/*
 * Method accepts the current number the program is attempting to plant,
 * the current row and the current column and checks within the box if 
 * the current number is already present
 */
bool Sudoku::numInBox(int cur, int cRow, int cColumn) const {
    int rowRoot = sqrt(ROWS);
    int colRoot = sqrt(COLUMNS);
    for (int i = (cRow/rowRoot) * rowRoot; i<(cRow/rowRoot + 1)*rowRoot; i++) {
        for (int j = (cColumn/colRoot) * colRoot; j<(cColumn/colRoot + 1)*colRoot; j++) {
            if (puzzle[i][j] == cur)
                return true;
        }
    }
    return false;
}

/*
 * Method accepts the current number the program is attempting to plant,
 * the current row and the current column and checks with the other 
 * helper methods if the current number can be planted
 */
bool Sudoku::ableToPlant(int cur, int cRow, int cColumn) const {
    return !numInRow(cur, cRow) && !numInColumn(cur, cColumn) && !numInBox(cur, cRow, cColumn);
}
