import edu.princeton.cs.algs4.StdRandom;
import edu.princeton.cs.algs4.StdStats;

public class PercolationStats {

    private double[] percentage;
    private int numberOfTrials;

    // perform independent trials on an n-by-n grid
    public PercolationStats(int n, int trials){
        if(n <= 0 || trials <= 0) {
            throw new IllegalArgumentException();
        }
        numberOfTrials = trials;
        percentage = new double[trials];

        for(int i = 0; i < trials; i++){
            Percolation percolation = new Percolation(n);

            while(!percolation.percolates()){
                percolation.open(StdRandom.uniform(1, n + 1), StdRandom.uniform(1, n + 1));
            }

            percentage[i] = (double)percolation.numberOfOpenSites() / (n * n);
        }
    }

    // sample mean of percolation threshold
    public double mean(){
        return StdStats.mean(percentage);
    }

    // sample standard deviation of percolation threshold
    public double stddev(){
        return StdStats.stddev(percentage);
    }

    // low endpoint of 95% confidence interval
    public double confidenceLo(){
        return mean() - ((1.96 * stddev()) / Math.sqrt(numberOfTrials));
    }

    // high endpoint of 95% confidence interval
    public double confidenceHi(){
        return mean() + ((1.96 * stddev()) / Math.sqrt(numberOfTrials));
    }

    // test client (see below)
    public static void main(String[] args){
        int n = Integer.parseInt(args[0]);
        int trials = Integer.parseInt(args[1]);
        PercolationStats ps = new PercolationStats(n, trials);

        System.out.println("mean\t\t\t\t\t= " + ps.mean());
        System.out.println("stddev\t\t\t\t\t= " + ps.stddev());
        System.out.println("95% confidence interval = " + ps.confidenceLo() + ", " + ps.confidenceHi());
    }

}