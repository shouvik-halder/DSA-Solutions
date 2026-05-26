public class Solution {
    public string MergeAlternately(string word1, string word2) {
    int l1 = 0, l2 = 0;
    string output = "";
    
    while (l1 < word1.Length && l2 < word2.Length) {
        output += word1[l1];
        output += word2[l2];
        l1++; 
        l2++;
    }
    
    return output + word1.Substring(l1) + word2.Substring(l2);
}

}