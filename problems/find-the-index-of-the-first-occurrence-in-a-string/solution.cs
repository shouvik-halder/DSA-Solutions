public class Solution {
    public int StrStr(string haystack, string needle) {
        // brute
        // int n = haystack.Length;
        // int m = needle.Length;
        // for(int i = 0; i<=n-m;i++){
        //     int j= 0 ;
        //     while(j<m && haystack[i+j]==needle[j]){
        //         j++;
        //     }
        //     if(j==m){
        //         return i;
        //     }
        // }
        // return -1;

        // optimised
        // knutt-matt-pratt algo

        int n = haystack.Length;
        int m = needle.Length;
        var lps = BuildLPS(needle, m);
        int i = 0;
        int j = 0;

        while(i<n){
            if(haystack[i]==needle[j]){
                i++;j++;
            }

            if(j==m){
                return i-j;
            }
            else if(i < n && haystack[i]!=needle[j]){
                if(j>0){
                    j = lps[j-1];

                }
                else{
                    i++;
                }
            }
        }
        return -1;

    }

    public int[] BuildLPS(string pat, int m){
        int[] lps = new int[m];
        lps[0]=0;
        int j = 1, len=0;
        while(j<m){
            if(pat[j]==pat[len]){
                len++;
                lps[j]=len;
                j++;
            }
            else {
                if(len>0){
                    len = lps[len-1];
                }
                else{
                    lps[j]=0;
                    j++;
                }
            }
        }

        return lps;
    }
}