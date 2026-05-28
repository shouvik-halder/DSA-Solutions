public class Solution {
    public bool IsAnagram(string s, string t) {
        if (s.Length != t.Length) return false;

        int[] count = new int[26];

        foreach (char ch in s) {
            count[ch - 'a']++;
        }

        foreach (char ch in t) {
            count[ch - 'a']--;
            if (count[ch - 'a'] < 0) return false;
        }

        return true;
    }
}