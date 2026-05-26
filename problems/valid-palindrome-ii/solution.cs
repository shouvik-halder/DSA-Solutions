public class Solution {
    public bool ValidPalindrome(string s) {
        int l=0,r=s.Length-1;
        while(l<r)
        {
            if(s[l]!=s[r]){
                return IsPalindrome(s,l + 1, r) || IsPalindrome(s,l, r - 1);
            }
            l++;r--;
        }
        return true;
    }

    public bool IsPalindrome(string s, int l, int r){
        while (l < r) {
                if (s[l] != s[r]) return false;
                l++;
                r--;
            }
            return true;
    }
    }

