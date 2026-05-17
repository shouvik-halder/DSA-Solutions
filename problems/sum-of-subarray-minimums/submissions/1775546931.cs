public class Solution {
    public int SumSubarrayMins(int[] arr) {
        int[] nse = findNse(arr);
        int[] psee = findPsee(arr);
        long MOD = (long)1e9 + 7;
        long sum = 0;

        for(int i = 0; i < arr.Length; i++){
            int left = i - psee[i];
            int right = nse[i] - i;

            long contribution = ((long)left * right) % MOD;
            contribution = (contribution * arr[i]) % MOD;

            sum = (sum + contribution) % MOD;
        }

        return (int)sum;
    }

    int[] findNse(int[] arr){
        Stack<int> st = new Stack<int>();
        int n = arr.Length;
        int[] nse = new int[n];

        for(int i = n - 1; i >= 0; i--){
            while(st.Count != 0 && arr[st.Peek()] >= arr[i]){
                st.Pop();
            }
            nse[i] = st.Count == 0 ? n : st.Peek();
            st.Push(i);
        }

        return nse;
    }

    int[] findPsee(int[] arr){
        Stack<int> st = new Stack<int>();
        int n = arr.Length;
        int[] psee = new int[n];

        for(int i = 0; i < n; i++){
            while(st.Count != 0 && arr[st.Peek()] > arr[i]){
                st.Pop();
            }
            psee[i] = st.Count == 0 ? -1 : st.Peek();
            st.Push(i);
        }

        return psee;
    }
}