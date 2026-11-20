// 2021-22 Q2(a) — Decorator: each layer wraps the packet and adds its header (data-link also a trailer)
class Packet {
    final String message;
    Packet(String m) { message = m; }
    int length() { return message.length(); }
    public String toString() { return "message: " + message + ", length: " + length(); }
}
interface Layer { Packet send(String msg); }                 // component

class RawPacket implements Layer {                            // concrete component: user's Packet
    public Packet send(String msg) { return new Packet(msg); }
}
abstract class LayerDecorator implements Layer {              // base decorator
    protected final Layer inner;
    LayerDecorator(Layer inner) { this.inner = inner; }
}
class ApplicationLayer extends LayerDecorator {
    ApplicationLayer(Layer l) { super(l); }
    public Packet send(String m) { return new Packet("APPHEADER_" + inner.send(m).message); }
}
class TransportLayer extends LayerDecorator {
    TransportLayer(Layer l) { super(l); }
    public Packet send(String m) { return new Packet("TRHEADER_" + inner.send(m).message); }
}
class NetworkLayer extends LayerDecorator {
    NetworkLayer(Layer l) { super(l); }
    public Packet send(String m) { return new Packet("NETHEADER_" + inner.send(m).message); }
}
class DataLinkLayer extends LayerDecorator {
    DataLinkLayer(Layer l) { super(l); }
    public Packet send(String m) { return new Packet("DHEADER_" + inner.send(m).message + "_DTRAILER"); }
}
class PhysicalLayer extends LayerDecorator {
    PhysicalLayer(Layer l) { super(l); }
    public Packet send(String m) { return new Packet("PHEADER_" + inner.send(m).message); }
}
public class NetworkStack {
    public static void main(String[] args) {
        Layer stack = new PhysicalLayer(new DataLinkLayer(new NetworkLayer(
                      new TransportLayer(new ApplicationLayer(new RawPacket())))));
        System.out.println(new RawPacket().send("hello"));
        System.out.println(new ApplicationLayer(new RawPacket()).send("hello"));
        System.out.println(stack.send("hello"));
    }
}
