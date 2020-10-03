#! python3

path = 'etherscan.output'

TotalBlock = 0
TotalTransactions = 0
TotalContractTx = 0
TotalBytes = 0

with open(path, 'r') as f:
    for i in range(3):
        f.readline()
    for line in f.readlines():
        output = line.split()
        TotalBlock += 1
        TotalTransactions += int(output[1])
        TotalContractTx += int(output[2])
        TotalBytes += int("".join(output[3].split(',')))

print("====================")
print("Total Block: "+str(TotalBlock))
print("Total Transactions: "+str(TotalTransactions))
print("Total Contract Transactions: "+str(TotalContractTx))
print("Total Size(bytes): "+str(TotalBytes))
print("Total Size(MB): "+str(TotalBytes*1.0/1000000))
print("Average Block Size(bytes): "+str(TotalBytes/TotalBlock))
print("Average Transaction Size(bytes): "+str(TotalBytes/TotalTransactions))
print("Average Transactions in Block: "+str(TotalTransactions/TotalBlock))
print("====================")
