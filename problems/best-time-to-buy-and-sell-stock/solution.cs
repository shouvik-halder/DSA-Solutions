public class Solution {
    public int MaxProfit(int[] prices) {
        int profit =0, min=0, max=0;
        for(int i=0;i<prices.Length;i++){
            min=prices[i]<prices[min]?i:min;
            profit=Math.Max(profit,prices[i]-prices[min]);
        }
        return profit;
    }
}