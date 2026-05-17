public class Solution {
    public int[] NextGreaterElements(int[] nums) {
        int n = nums.Length;
        int[] res = new int[n];
        Array.Fill(res, -1);

        Stack<int> st = new Stack<int>();

        for (int i = 2 * n - 1; i >= 0; i--) {
            int num = nums[i % n];

            while (st.Count != 0 && st.Peek() <= num) {
                st.Pop();
            }

            if (i < n) {
                res[i] = st.Count == 0 ? -1 : st.Peek();
            }

            st.Push(num);
        }

        return res;
    }
}