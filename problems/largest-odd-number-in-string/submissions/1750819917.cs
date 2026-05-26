public class Solution {
    public string LargestOddNumber(string num) {
        for (int i = num.Length - 1; i >= 0; i--) {
            int digit = num[i] - '0'; // Convert char to int
            if (digit % 2 != 0) {
                // If an odd digit is found, the substring from the beginning
                // to this digit (inclusive) is the largest odd number.
                return num.Substring(0, i + 1);
            }
        }
        // If no odd digit is found, no odd number can be formed.
        return "";
    }
}