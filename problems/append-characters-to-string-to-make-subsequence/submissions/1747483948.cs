public class Solution {
    public int AppendCharacters(string s, string t) {
        int ls = s.Length;
        int lt = t.Length;
        int inds = 0;
        int indt = 0;
        while(inds<ls && indt<lt){
            if(t[indt]==s[inds]){
                indt++;
            }
            inds++;
        }
        if(indt<lt){
            return lt-indt;
        }
        return 0;
    }
}