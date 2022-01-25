# Data Analytics Project 2

### Arushi Mittal (2019101120) and Meghna Mishra (2019111030)

## Analysis of Runtimes

Hash: `0.010395050048828125`
Partition: `1636736242.157222` 
Standard: `0.0038979053497314453`

FPA: `0.0007143020629882812`
Standard: `0.0004508495330810547`

The datasets used were `tennis.txt` and `contextOpusMiner.txt` for testing purposes, and `chess.txt` for checking how the algorithm was working.

We used the following functions:
 - `Standard`: The standard library implementation of a priori from the `mlxtend.frequent_patterns` module.
 - `aprioriHash`: Our implementation of a priori with hashing
 - `aprioriPartition`: Our implementation of a priori with partitions.
 - `apriori`: Our standard implementation of a priori which requires the `getCount` function to give the inital itemset.
 - `fpa`: Our implementation of the fpa tree algorithm.
 - `pyfpgrowth.find_frequent_patterns`: The standard implementation of fpgrowth algorithm from the pyfpgrowth module.

## Implementation of Optimizations

The hash based approach involves multiplying the first order by 10 and adding to the second order, and taking modulo 7 to identify the hash index. The ocunt of each bucket is incremented and the hash is added to that particular bucket group. Later, only the itemsets from the buckets with the required count are stored and the rest are discarded. 

The partition based approach involves dividing into various partitions according to the user, and these partitions perform a priori independently. Later, the itemsets that are greater than minimum support in all the partitions are concatenated and after removal of the subsets, the final set of all closed frequent itemsets is returned.

The FP Algorithm involves finding all frequencies and then sorting in decreasing order. Aftre this, we use this decreasing order to construct our FP tree, and from this tree, we maintain the itemsets and their counts in a hierarchical and memory efficient manner. Once this is done, these values are used during the construction of the FPA tree, where the itemsets are ranked and placed on the branches of the FPA tree so they can be mined.

## Explanation of Analysis

The standard libraries obviously had the fastest runtime, however the apriori with hash implementation was not very far because a lot of time was saved in the beginning in the creation of frequent 1 and 2 itemsets. This pruning process made the whole procedure faster.

In the case of FPA, the standard implementation was faster, and overall both FPA implementations were faster than a priori because of using a tree-like structure that is easy to traverse and prune.