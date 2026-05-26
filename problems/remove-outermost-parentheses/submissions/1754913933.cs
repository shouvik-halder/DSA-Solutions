public class Solution {
    public string RemoveOuterParentheses(string s) {
        StringBuilder ans = new StringBuilder();
        int balance = 0;
        foreach(char character in s){
            if(character == '('){
                if(balance > 0){
                    ans.Append(character);
                }
                balance++;
            }
            else{
                balance--;
                if(balance > 0){
                    ans.Append(character);
                }
            }
        }
        return ans.ToString();
    }
}