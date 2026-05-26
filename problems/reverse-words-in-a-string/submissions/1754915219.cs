public class Solution {
    public string ReverseWords(string s) {
        string[] words = s.Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
         Array.Reverse(words);
         return string.Join(" ", words);
    //     s = s.Trim(); StringBuilder st = new StringBuilder(); int r=0;
    //     for(int i=s.Length-1;i>=0;i--){
    //         if(s[i]==' ' && r!=0){
    //             string word = s.Substring(i+1, r);
    //             st.Append(word+" "); r=0;
    //         }
    // else if(s[i]!=' '){
    //  r++;
    // }
    //     }
    //     st.Append(s.Substring(0, r));
    // return st.ToString();

    }
}