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
    public ListNode ReverseBetween(ListNode head, int left, int right) {
        if(left == right) return head;
        ListNode curr = head;
        ListNode dummy = new ListNode(0,head);
        ListNode prevLeft = dummy;
        while(left>1){
            curr = curr.next;
            prevLeft = prevLeft.next;
            left--;right--;
        }
        right = right - left +1;
        ListNode prev = null;

        while(right>0){
            ListNode tmp = curr.next;
            curr.next=prev;
            prev = curr;
            curr = tmp;
            right--; 
        }

        prevLeft.next.next = curr;
        prevLeft.next = prev;

        return dummy.next;
    }
}