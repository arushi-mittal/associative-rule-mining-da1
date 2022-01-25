import itertools
from math import floor, ceil
import time
from mlxtend.frequent_patterns import apriori as stdapriori
from mlxtend.preprocessing import TransactionEncoder

import pandas as pd


def getData (filename):
    '''
    Function to get the list of transactions from a particular filename.
    Inputs: The path of the file
    Outputs: The file data shared as a list of strings, where each string represents a single transaction.
    '''
    data = []
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    itemset = []
    for d in data:
        itemset.append(d.split(' '))  
        if '' in itemset[-1]:
            itemset[-1].remove('')
    return itemset

def getHash (transactions, minSupport) :
    '''
    Function to perform hashing to reduce time complexity of the algorithm. Each element of order 1
    is multiplied by 10 and added to element with order 0. The sum modulo 7 is used as the index for 
    the hash.
    '''
    hash = 7
    counts = [0 for i in range (hash)]
    buckets = [set([]) for i in range(hash)]
    items = []
    for transaction in transactions:
        combinations = list(itertools.combinations(transaction, 2))
        for combination in combinations:
            combination = sorted(list(combination))
            if combination[0] not in items:
                items.append(combination[0])
            if combination[1] not in items:
                items.append(combination[1])
            idx = (items.index(combination[0]) + items.index(combination[1]) * 10) % hash
            counts[idx] += 1
            buckets[idx].add(tuple(combination))
    hashset = []
    for i in range(hash) :
        if counts[i] >= minSupport:
            for item in buckets[i]:
                hashset.append(list(item))
            
    return hashset

def removeCommon (data):
    '''
    A function to remove all subsets from a superset so that only the closed frequent itemsets are
    returned.
    '''
    for large in data[::-1]:
        for small in data[:]:
            if large != small and set(small).issubset(large):
                data.remove(small)
    return data

def apriori (itemset, setSize, data, minSupport) :
    '''
    A function to run the a priori algorithm based on the given itemset, size of the next item set, 
    the transaction list, and the minimum support.
    '''
    minSupport *= ceil(len(data))
    nextIteration = True
    allItems = []
    while nextIteration:
        if setSize > 2:
            allItems += itemset
        nextItemSet = set([])
        itemSetSize = len(itemset)
        for i in range(itemSetSize):
            for j in range(i + 1, itemSetSize):
                if len(set(itemset[i] + itemset[j])) == setSize:
                    currentItem = tuple(sorted(set(itemset[i] + itemset[j])))
                    if currentItem not in nextItemSet:
                        nextItemSet.add(currentItem)
        if len(nextItemSet) == 0:
            nextIteration = False
            break

        counts = {}
        for transaction in data:
            for item in nextItemSet:
                if set(item).issubset(set(transaction)):
                    if item in counts:
                        counts[item] += 1
                    else:
                        counts[item] = 1
        
        if len(counts) == 0:
            nextIteration = False
            break 
        nextItemSet = []
        for count in counts:
            if counts[count] >= minSupport:
                nextItemSet.append(list(count))
        if len(nextItemSet) == 0:
            nextIteration = False
            break
        itemset = nextItemSet
        setSize += 1
    print("done")
    return allItems


def aprioriHash (filename, minSupport) :
    '''
    Function to perform A Priori algorithm on a given dataset.
    Inputs: Input file name, Minimum Support Percentage, Minimum Confidence Percentage
    Outputs: A list of associations after performing A Priori algorithm on the given dataset.
    '''
    data = getData(filename)
    records = len(data)
    itemset = getHash(data, floor(minSupport * records))
    allItems = apriori(itemset, 3, data, minSupport)

    allItems = removeCommon(allItems)
    return allItems


############ PARTITION FUNCTIONS ###############

def makePartition(a, n):
    '''
    Function to partition a list into n divisions of equal sizes as far as possible.
    '''
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def getCount (transactions, minSupport) :
    minSupport = ceil(minSupport * len(transactions))
    itemset = {}
    for transaction in transactions:
        for item in transaction:
            if item not in itemset:
                itemset[item] = 1
            else:
                itemset[item] += 1
    data = []
    for item in itemset:
        if itemset[item] >= minSupport:
            data.append(item)
    return data


def aprioriPartition (filename, minSupport, partitions) :
    transactions = getData(filename)
    partitions = list(makePartition(transactions, partitions))
    results = []
    for partition in partitions:
        itemset = getCount(partition, minSupport)
        itemset = [[item] for item in itemset]
        results += apriori(itemset, 2, partition, minSupport)
    results = list(set([tuple(res) for res in results]))
    results = removeCommon(results)
    return results

def standard (filename, minSupport) :
    te = TransactionEncoder()
    dataset = getData(filename)
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    stdapriori(df, min_support=minSupport)

# aprioriPartition('test_files/contextOpusMiner.txt', 0.6, 5)
# print('\n\n\n\n')
# aprioriHash('./test_files/contextOpusMiner.txt', 0.6)
# aprioriPartition('test_files/tennis.txt', 0.4, 5)
# print('\n\n\n\n')
# aprioriHash('./test_files/tennis.txt', 0.4)
filename = './test_files/tennis.txt'
start = time.time()
aprioriHash(filename, 0.5)
hashtime = time.time() - start
aprioriPartition(filename, 0.5, 5)
partitiontime = time.time() - hashtime
standard(filename, 0.5)
stdtime = time.time() - partitiontime
print(hashtime, partitiontime, stdtime)