#1) Read excel
#2) Filter to 20210500
#3) Go through to see what the best worth is

df = pd.read_pickle("~/ski/elo/python/ski/ladies/varladies.pkl")
df = df.loc[df['date']=='20210500']

def knapSack(W, wt, val, n, lim): 
  
    # Base Case 
    if n == 0 or W == 0 : 
        return 0
  
    # If weight of the nth item is more than Knapsack of capacity 
    # W, then this item cannot be included in the optimal solution 
    if (wt[n-1] > W): 
        return knapSack(W, wt, val, n-1) 
  
    # return the maximum of two cases: 
    # (1) nth item included 
    # (2) not included 
    else: 
        return max(val[n-1] + knapSack(W-wt[n-1], wt, val, n-1), 
                   knapSack(W, wt, val, n-1)) 

wc = [100, 80, 60, 50, 45, 40, 36, 32, 29, 26, 24, 22, 20, 18, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

stage = [50, 46, 43, 40, 37, 34, 32, 30, 28, 26, 24, 20, 18, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

opening = [200, 160, 120, 100, 90, 80, 72, 64, 58, 52, 48, 44, 40, 36, 32, 30, 28, 26, 24, 22, 20, 18, 16, 14, 12, 10, 8, 6, 4, 2] 

tour = [400, 320, 240, 200, 180, 160, 144, 128, 116, 104, 96, 88, 80, 72, 64, 60, 56, 52, 48, 44, 40, 36, 32, 28, 24, 20, 20, 20, 20, 20, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

