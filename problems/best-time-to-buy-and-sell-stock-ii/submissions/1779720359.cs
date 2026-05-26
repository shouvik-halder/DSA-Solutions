public class Solution {
    public int MaxProfit(int[] prices) {
        // brute
        // return Solve(prices, 0, false);
        int profit = 0;
        for(int i = 1; i<prices.Length;i++){
            if(prices[i]>prices[i-1]){
                profit+=prices[i]-prices[i-1];
            }
        }
        return profit;
    }
    // brute
    public int Solve(int[] prices, int day, bool holding){
        if (day == prices.Length) return 0;
        if(holding){
            int sell = prices[day]+Solve(prices, day+1, false);
            int hold = Solve(prices, day+1,true);
            return Math.Max(sell, hold);
        }
        else{
            int buy = -prices[day]+Solve(prices, day+1, true);
            int skip = Solve(prices, day+1,false);
            return Math.Max(buy, skip);
        }
    }


}