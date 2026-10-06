class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def hasCycle(head: ListNode) -> bool:
    conj = set()
    actual = head
    while actual is not None:
        if actual in conj:
            return True
        conj.add(actual)
        actual = actual.next
    return False


class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        return hasCycle(head)     
        