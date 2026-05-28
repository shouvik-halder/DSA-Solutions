public class Solution
{
    public bool IsPalindrome(string s)
    {
        int l = 0, r = s.Length - 1;

        while (l < r)
        {
            if (!IsAlphaNum(s[l]))
            {
                l++;
            }
            else if (!IsAlphaNum(s[r]))
            {
                r--;
            }
            else if (char.ToLower(s[l]) != char.ToLower(s[r]))
            {
                return false;
            }
            else
            {
                l++;
                r--;
            }
        }

        return true;
    }

    public bool IsAlphaNum(char ch)
    {
        return (ch >= 'A' && ch <= 'Z') ||
               (ch >= 'a' && ch <= 'z') ||
               (ch >= '0' && ch <= '9');
    }
}