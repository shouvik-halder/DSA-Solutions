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
    public ListNode ReverseList(ListNode head) {
        ListNode temp = head, prev = null;
        while(temp!=null){
            ListNode front = temp.next;
            temp.next = prev;
            prev= temp;
            temp = front;
        }
        return prev;
    }
}