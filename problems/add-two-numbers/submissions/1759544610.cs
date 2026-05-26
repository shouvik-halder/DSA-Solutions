/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     public int val;
 *     public ListNode next;
 *     public ListNode(int val=0, ListNode next=null) {
 *         this.val = val;
 *         this.next = next;
 *     }
 * }
 */
public class Solution {
    public ListNode AddTwoNumbers(ListNode l1, ListNode l2) {
        ListNode res = new ListNode(0);
        ListNode head = res;
        int rem = 0;
        while(l1!=null || l2 !=null || rem>0){
            int x = l1 ==null?0:l1.val;
            int y = l2 ==null?0:l2.val;
            int sum = x+y+rem;
            rem = sum/10;
            head.next = new ListNode(sum %=10);
            l1=l1?.next;
            l2 = l2?.next;
            head = head.next;
        }

        return res.next;
    }
}