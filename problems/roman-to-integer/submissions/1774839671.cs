public class Solution {
    public int RomanToInt(string s) {
        int result = 0;

        for (int i = 0; i < s.Length; i++) {
            int current = RomanHelper(s[i]);

            if (i + 1 < s.Length && current < RomanHelper(s[i + 1])) {
                result -= current;
            } else {
                result += current;
            }
        }

        return result;
    }

    private int RomanHelper(char ch){
        switch(ch){
            case 'I': return 1;
            case 'V': return 5;
            case 'X': return 10;
            case 'L': return 50;
            case 'C': return 100;
            case 'D': return 500;
            case 'M': return 1000;
            default: return 0;
        }
    }
}