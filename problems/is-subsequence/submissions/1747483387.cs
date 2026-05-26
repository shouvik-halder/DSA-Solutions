public class Solution {
    public bool IsSubsequence(string s, string t) {
        int ls = s.Length; 
        int lt = t.Length;
        int inds=0; int indt = 0;
        while(inds<ls && indt<lt){
            if(s[inds]==t[indt]){
                inds++;
            }
            indt++;
        }
        return inds==ls;
    }
}