public class Solution {
    public int LongestPalindrome(string s) {
        HashSet<char> oddChars = new HashSet<char>();
        int len = 0;
        foreach(char ch in s){
            if(oddChars.Contains(ch)){
                oddChars.Remove(ch);
                len+=2;
            }
            else oddChars.Add(ch);
        }

        if(oddChars.Count>0) len++;

        return len;
    }
}