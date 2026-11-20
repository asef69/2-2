// 2010-11 Q6(e) — test cases for a Queue class
import static org.junit.Assert.*;
import org.junit.Before;
import org.junit.Test;

public class QueueTest {
    private BoundedQueue<Integer> q;
    @Before public void setUp() { q = new BoundedQueue<>(3); }

    @Test public void newQueue_isEmpty() { assertTrue(q.isEmpty()); assertEquals(0, q.size()); }
    @Test public void fifoOrder() {
        q.enqueue(1); q.enqueue(2); q.enqueue(3);
        assertEquals(Integer.valueOf(1), q.dequeue());
        assertEquals(Integer.valueOf(2), q.dequeue());
    }
    @Test public void wrapAround_keepsOrder() {
        q.enqueue(1); q.enqueue(2); q.dequeue(); q.enqueue(3); q.enqueue(4);
        assertEquals(Integer.valueOf(2), q.dequeue());
        assertEquals(Integer.valueOf(3), q.dequeue());
        assertEquals(Integer.valueOf(4), q.dequeue());
    }
    @Test(expected = IllegalStateException.class) public void dequeueEmpty_throws() { q.dequeue(); }
    @Test(expected = IllegalStateException.class) public void enqueueFull_throws() {
        q.enqueue(1); q.enqueue(2); q.enqueue(3); q.enqueue(4);
    }
    @Test(expected = IllegalArgumentException.class) public void zeroCapacity_throws() { new BoundedQueue<Integer>(0); }
}
