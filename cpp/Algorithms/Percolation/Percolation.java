import edu.princeton.cs.algs4.WeightedQuickUnionUF;

/*
    Considering an N by N grid, where each square can be open or closed (true or false),
    a percolation check basically checks if there is a path of adjacent open squares that go from the first row
    to the bottom row.
    E.g.    X O X X     X O X X
            X O X X     X O O X
            X X X X     X O O X
            X X X X     X X O X
    doesn't percolate  does percolate

    In this example, the grid starts all closed and a new square is opened each round, and each round a check is made
    to see if the grid percolates.

    The fastest way to check this is by using UnionFind, where if a square in the top row is connected to a square
    in the bottom row, this means the grid percolates.

    To prevent having to check each square in the top and bottom square, it is considered that above the top row there
    is a square, which parents all the top row, and bellow the bottom row, there is a square that parents all the
    bottom row. This way, if the "toptop" square is ever connected to the "bottombottom" square, that means that some
    square in the top row is connected to some square in the bottom row, meaning we have percolation.

    Edit: Added second UnionFind to prevent "backwash" when checking for connection.
    Backwash basically means that an isolated (usually bottom) part of the grid is connected to the top through
    the bottombottom square.
    E.g:    X X X X O
            X X X X O
            X X X X O
            X X X X O
            O X X X O
            ^ This part returns True to isFull() due to a connection going through the bottombottom square.
 */

public class Percolation {

    private boolean[][] grid; // true == open
    private WeightedQuickUnionUF unionFind, nonBackWashUnionFind;
    private int top, bottom, size;

    // creates n-by-n grid, with all sites initially blocked
    public Percolation(int n) {
        if(n <= 0){
            throw new IllegalArgumentException();
        }

        unionFind = new WeightedQuickUnionUF(n * n + 2); // +2 is for the toptop and bottombottom squares.
        nonBackWashUnionFind = new WeightedQuickUnionUF(n * n + 1); //
        grid = new boolean[n][n];
        top = 0;
        bottom = n * n + 1;
        size = n;
    }

    // opens the site (row, col) if it is not open already
    public void open(int row, int col){
        if(row < 1 || size < row || col < 1 || size < col) {
            throw new IllegalArgumentException();
        }

        grid[row - 1][col - 1] = true;

        if(row == 1){
            unionFind.union(gridToIndex(row,col), top);
            nonBackWashUnionFind.union(gridToIndex(row,col), top);
        }

        if(row == size){
            unionFind.union(gridToIndex(row,col), bottom);
        }

        if(col != 1 && isOpen(row, col - 1)){
            unionFind.union(gridToIndex(row,col), gridToIndex(row,col-1));
            nonBackWashUnionFind.union(gridToIndex(row,col), gridToIndex(row,col-1));
        }

        if(col != size && isOpen(row, col + 1)){
            unionFind.union(gridToIndex(row,col), gridToIndex(row,col+1));
            nonBackWashUnionFind.union(gridToIndex(row,col), gridToIndex(row,col+1));
        }

        if(row != 1 && isOpen(row - 1, col)){
            unionFind.union(gridToIndex(row,col), gridToIndex(row - 1,col));
            nonBackWashUnionFind.union(gridToIndex(row,col), gridToIndex(row - 1,col));
        }

        if(row != size && isOpen(row + 1, col)){
            unionFind.union(gridToIndex(row,col), gridToIndex(row + 1,col));
            nonBackWashUnionFind.union(gridToIndex(row,col), gridToIndex(row + 1,col));
        }

    }

    // is the site (row, col) open?
    public boolean isOpen(int row, int col){
        if(row < 1 || size < row || col < 1 || size < col) {
            throw new IllegalArgumentException();
        }
        return grid[row-1][col-1];
    }

    // is the site (row, col) full?
    public boolean isFull(int row, int col){
        if(row < 1 || size < row || col < 1 || size < col) {
            throw new IllegalArgumentException();
        }
        return nonBackWashUnionFind.connected(gridToIndex(row, col), top);
    }

    // returns the number of open sites
    public int numberOfOpenSites(){
        int count = 0;
        for(int i = 0; i < size; i++){
            for(int j = 0; j < size; j++){
                if(grid[i][j]){
                    count++;
                }
            }
        }
        return count;
    }

    // does the system percolate?
    public boolean percolates(){
        return unionFind.connected(top, bottom);
    }

    private int gridToIndex(int row, int col){
        return size * (row - 1) + (col);
    }
}