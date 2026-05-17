public class Solution {
    public int[] NextGreaterElement(int[] nums1, int[] nums2) {
        Dictionary<int, int> neg = new Dictionary<int, int>(); 
        int[] res = new int[nums1.Length];
        Stack<int> st = new Stack<int>();

        int i = nums2.Length - 1;

        while (i >= 0) {
            while (st.Count != 0 && st.Peek() <= nums2[i]) {
                st.Pop();
            }

            if (st.Count == 0)
                neg[nums2[i]] = -1;
            else
                neg[nums2[i]] = st.Peek();

            st.Push(nums2[i]);
            i--;
        }

        for (int j = 0; j < nums1.Length; j++) {
            res[j] = neg[nums1[j]];
        }

        return res;
    }
}