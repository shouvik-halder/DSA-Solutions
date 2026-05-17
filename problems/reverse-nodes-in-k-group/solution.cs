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
    public ListNode ReverseKGroup(ListNode head, int k) {
        if (head == null) return head;

        ListNode temp = head, end = head;
        int counter = k;

        // Move 'end' to kth node
        while (counter > 1 && end != null) {
            end = end.next;
            counter--;
        }

        // If less than k nodes
        if (end == null) return head;

        ListNode nextGroup = end.next;
        end.next = null;

        // Reverse current k group
        ListNode newHead = reverse(temp);

        // Connect with next groups
        temp.next = ReverseKGroup(nextGroup, k);

        return newHead;
    }

    ListNode reverse(ListNode head) {
        if (head == null || head.next == null) return head;

        ListNode newHead = reverse(head.next);
        head.next.next = head;
        head.next = null;

        return newHead;
    }
}