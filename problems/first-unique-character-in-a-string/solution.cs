public class Solution {
    public int FirstUniqChar(string s) {
        int[] freq = new int[26];
        foreach(char ch in s){
            freq[ch-'a']++;
        }

        foreach(char ch in s){
            if(freq[ch-'a']==1){
                return s.IndexOf(ch);
            }
        }
        return -1;
    }
}