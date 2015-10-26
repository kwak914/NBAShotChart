// Henry Bogardus
// CS 270
// Project 1 - Sudoku Solver
// Honor Statement - "I did not give or receive any unauthorized help on this assignment."

#ifndef SUDOKU_H
#define SUDOKU_H

#include <iostream>
#include <string>
#include <tuple>
using namespace std;


class Sudoku
{
private:
    const int ROWS = 9;
    const int COLUMNS = 9;
    int ** puzzle;
    
public:
    Sudoku();               // default ctor
    void loadFromFile(string filename);
    bool solve();
    void print() const;
    bool equals(const Sudoku &other) const;
    bool recursiveSolve(int cRow, int cColumn);
    bool boardFilled() const;
    bool numInRow(int cur, int cRow) const;
    bool numInColumn(int cur, int cColumn) const;
    bool numInBox(int cur, int cRow, int cColumn) const;
    bool ableToPlant(int cur, int cRow, int cColumn) const;
};
#endif
