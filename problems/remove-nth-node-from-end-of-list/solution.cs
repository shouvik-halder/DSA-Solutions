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
    public ListNode RemoveNthFromEnd(ListNode head, int n) {
        ListNode curr = head;
        int length = 0;
        while(curr!=null){
            ++length;curr= curr.next;
        }

        int traverseLength = length-n-1;
        curr = head;
        if(traverseLength==-1){
            return head.next;
        }
        while(traverseLength>0){
            curr = curr.next;--traverseLength;
        }
        curr.next = curr.next.next;
        return head;
    }
}