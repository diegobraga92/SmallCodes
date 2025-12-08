# Fibonacci

Simple code, just build an array of size n (Fibonacci request number) in a straight loop.

A standard recursive approach causes a lot of unneeded recalculation.

# Fibonacci Mod

This problem expects huge inputs, so calculating the whole Fibonacci becomes unfeasible.

Instead it's used the Pisano Period, which basically states that the mod(%) "m" of the Fibonacci series follows a standard.

The first step in this is to discover the period, which always starts with 0 1. 

With the period length found, it's only necessary to compute the fibonacci series up to period length, or, even better, up to the remainder of the input number divided by the mod.

Also, like when calculating the last digit, the mod can be calculated by adding the previous two remainders and applying the mod again, preventing the storage of huge numbers.

This code can be adapted to calculated the last digit of the sum of a huge fibonacci number, by using mod 10 and getting the sum of the period.

