#This code is used to calculate the Z score and Z'' score

def dot(K, L):
   if len(K) != len(L):
      return 0

   return sum(i[0] * i[1] for i in zip(K, L))
#initialize required variables

CA = float(input("Enter Current Assets: "))
CL = float(input("Enter Current Liabilities: "))
TA = float(input("Enter Total Assets: "))
RE = float(input("Enter Retained Earnings: "))
EBIT = float(input("Enter EBIT: "))
BVE = float(input("Enter total stockholders equity: "))
AS = float(input("Enter the number of authorized shares: "))
P = float(input("Enter the share price at the time of statement filing: "))
L = float(input("Enter the Total Liabilities: "))
Sales = float(input("Enter the Sales or Revenue: "))

#Construct required variables for calculation
NWC = CA - CL
MVE = (P*AS)/1000
RE = RE+EBIT

#initialize the required Z-score coefficients and variables
ZcoeffList = [1.2,1.4,3.3,.6,1]
ZVarList = [NWC/TA, RE/TA, EBIT/TA, MVE/L, Sales/TA]

ZPrimecoeffList = [6.56,3.26,6.72,1.05]
ZPrimeVarList = [NWC/TA,RE/TA,EBIT/TA,BVE/L]

print(ZVarList)
print(ZPrimeVarList)
#Calculate the Z-scores
print("The Z score was",dot(ZcoeffList,ZVarList))
print("The Z'' socre was",dot(ZPrimecoeffList,ZPrimeVarList))

print("For Z-score: below 1.8 is bad - above 3 is good.")
print("For Z''score: below 1.6 is bad - above 2.6 is good.")
