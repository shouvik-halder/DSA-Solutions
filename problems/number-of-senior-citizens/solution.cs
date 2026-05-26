public class Solution {
    public int CountSeniors(string[] details) {
        int c = 0;
        for(int i=0;i<details.Length;i++){
            c = c + (((details[i][11] - '0') * 10 + (details[i][12] - '0')) > 60 ? 1 : 0);
        }
        return c;
    }
}