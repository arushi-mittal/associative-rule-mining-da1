import time
import pyfpgrowth


class Node:
    def __init__(self, itemName, frequency, parentNode):
        self.itemName = itemName
        self.count = frequency
        self.parent = parentNode
        self.children = {}
        self.next = None

    def increment(self, frequency):
        self.count += frequency

    def display(self, ind=1):
        print('  ' * ind, self.itemName, ' ', self.count)
        for child in list(self.children.values()):
            child.display(ind+1)


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

def getCount (transactions, minSupport) :
    records = len(transactions)
    minSupport *= records
    itemset = {}
    for transaction in transactions:
        for item in transaction:
            if item not in itemset:
                itemset[item] = 1
            else:
                itemset[item] += 1
    data = {}
    for item in itemset:
        if itemset[item] >= minSupport:
            data[item] = itemset[item]
    return data

def fpa (filename, minSupport) :
    transactions = getData(filename)
    itemset = getCount(transactions, minSupport)
    itemset = dict(sorted(itemset.items(), key=lambda item: -1 * item[1]))
    allowedItems = list(itemset.keys())

    nextTransactions = []

    for transaction in transactions:
        transaction = list(set(allowedItems).intersection(transaction))
        transaction.sort(key = lambda x: -1 * itemset[x])
        nextTransactions.append(transaction)

    fpTree = Node('Null', 1, None)
    for transaction in nextTransactions:
        currentNode = fpTree
        for item in transaction:
            if item in currentNode.children:
                currentNode.children[item].increment(itemset[item])
            else:
                newNode = Node (item, itemset[item], currentNode)
                currentNode.children[item] = newNode

    fpTree.display()

    
start = time.time()
fpa('./test_files/tennis.txt', 0.3)
fpatime = time.time() - start

patterns = pyfpgrowth.find_frequent_patterns(getData('./test_files/tennis.txt'), 0.3)
stdtime = time.time() - fpatime
print(fpatime, stdtime)