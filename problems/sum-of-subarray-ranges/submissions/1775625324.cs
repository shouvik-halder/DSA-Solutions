public class Solution {
    public long SubArrayRanges(int[] nums) {
        int[] nse = findNse(nums);
        int[] psee = findPsee(nums);
        int[] nge = findNge(nums);
        int[] pgee = findPgee(nums);

        int n = nums.Length;long sum = 0;

for(int i = 0; i < n; i++){
    long smallLeft = i - psee[i];
    long smallRight = nse[i] - i;
    long largeLeft = i - pgee[i];
    long largeRight = nge[i] - i;

    long smallContribution = smallLeft * smallRight * nums[i];
    long largeContribution = largeLeft * largeRight * nums[i];

    sum += (largeContribution - smallContribution);
}

        return sum;
    }

    int[] findNse(int[] arr){
        int n = arr.Length;int i = n-1; 
        Stack<int> st = new Stack<int>();
        int[] nse = new int[n];
        while(i>=0){
            while(st.Count!=0 && arr[st.Peek()]>=arr[i]){
                st.Pop();
            }

            nse[i] = st.Count==0?n:st.Peek();
            st.Push(i);
            i-=1;
        }
        return nse;
    }

    int[] findPsee(int[] arr){
        Stack<int> st = new Stack<int>();
        int n=arr.Length; int[] psee = new int[n];

        for(int i=0;i<n;i++){
            while(st.Count!=0 && arr[st.Peek()]>arr[i]){
                st.Pop();
            }
            psee[i] = st.Count==0?-1:st.Peek();
            st.Push(i);
        }
        return psee;
    }

    int[] findNge(int[] arr){
        Stack<int> st = new Stack<int>();int n = arr.Length;
        int[] nge = new int[n];int i = n-1;

        while(i>=0){
            while(st.Count!=0 && arr[st.Peek()]<=arr[i]){
                st.Pop();
            }
            nge[i] = st.Count==0?n:st.Peek();
            st.Push(i);
            i-=1;
        }

        return nge;
    }

    int[] findPgee(int[] arr){
        Stack<int> st = new Stack<int>();
        int n=arr.Length; int[] pgee = new int[n];

        for(int i=0;i<n;i++){
            while(st.Count!=0 && arr[st.Peek()]<arr[i]){
                st.Pop();
            }
            pgee[i] = st.Count==0?-1:st.Peek();
            st.Push(i);
        }
        return pgee;
    }
}