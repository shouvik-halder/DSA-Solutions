public class Solution {
    public int PasswordStrength(string password) {

        HashSet<char> charr = new HashSet<char>();

        foreach (char ch in password) {
            charr.Add(ch);
        }

        int sum = 0;

        foreach (char ch in charr) {
            sum += Points(ch);
        }

        return sum;
    }

    public int Points(char ch) {

    if (char.IsUpper(ch))
        return 2;

    if (char.IsLower(ch))
        return 1;

    if (char.IsDigit(ch))
        return 3;

    if ("!@#$".Contains(ch))
        return 5;

    return 0;
}
}