public class Solution {
    public bool CanConstruct(string ransomNote, string magazine) {
        int[] freq  = new int[26];
        foreach(char ch in magazine){
            freq[ch-'a']++;
        }

        foreach(char ch in ransomNote){
            if(freq[ch-'a']==0) return false;
            else freq[ch-'a']--;
        }
        return true;
    }
}