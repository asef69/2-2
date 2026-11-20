public class BoundedQueue<T> {
    private final Object[] data; private int head, size;
    public BoundedQueue(int capacity) {
        if (capacity <= 0) throw new IllegalArgumentException();
        data = new Object[capacity];
    }
    public void enqueue(T x) {
        if (size == data.length) throw new IllegalStateException("full");
        data[(head + size++) % data.length] = x;
    }
    @SuppressWarnings("unchecked")
    public T dequeue() {
        if (size == 0) throw new IllegalStateException("empty");
        T x = (T) data[head]; data[head] = null; head = (head + 1) % data.length; size--;
        return x;
    }
    public boolean isEmpty() { return size == 0; }
    public int size() { return size; }
}
