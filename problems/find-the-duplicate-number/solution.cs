public class Solution {
    public int FindDuplicate(int[] nums) {
        // int slow = nums[0];
        // int fast = nums[0];
        // while(true){
        //     slow = nums[slow];
        //     fast = nums[nums[fast]];
        //     if(slow == fast){
        //         break;
        //     }
        // }

        // int slow2=0;
        // while(true){
        //     slow2 = nums[slow2];
        //     slow = nums[slow];
        //     if(slow == slow2){
        //         return slow;
        //     }
        // }

        int slow = nums[0];
        int fast = nums[0];

        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);

        slow = nums[0];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }

        return slow;
    }
}