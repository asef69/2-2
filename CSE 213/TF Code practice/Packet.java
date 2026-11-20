interface Packet {
    String getMessage();

    int getLength();
}

class SimplePacket implements Packet {
    private final String message;

    SimplePacket(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }

    public int getLength() {
        return message.length();
    }
}

abstract class LayerDecorator implements Packet {
    protected final Packet inner;

    LayerDecorator(Packet packet) {
        this.inner = packet;
    }

    public abstract String getMessage();

    public int getLength() {
        return getMessage().length();
    }
}

class ApplicationLayer extends LayerDecorator {
    ApplicationLayer(Packet packet) {
        super(packet);
    }

    public String getMessage() {
        return "APPHEADER_" + inner.getMessage();
    }
}

class TransportLayer extends LayerDecorator {
    TransportLayer(Packet packet) {
        super(packet);
    }

    public String getMessage() {
        return "TRHEADER_" + inner.getMessage();
    }
}

class NetworkLayer extends LayerDecorator {
    NetworkLayer(Packet packet) {
        super(packet);
    }

    public String getMessage() {
        return "NETHEADER_" + inner.getMessage();
    }
}

class DataLinkLayer extends LayerDecorator {
    DataLinkLayer(Packet packet) {
        super(packet);
    }

    public String getMessage() {
        return "DHEADER_" + inner.getMessage() + "_DTRAILER";
    }
}

class PhysicalLayer extends LayerDecorator {
    PhysicalLayer(Packet packet) {
        super(packet);
    }

    public String getMessage() {
        return "PHEADER_" + inner.getMessage();
    }
}

class NetworkModel {
    static void show(String stage, Packet packet) {
        System.out.println(stage + " -> message: " + packet.getMessage()
                + ", length: " + packet.getLength());
    }

    public static void main(String[] args) {
        Packet packet = new SimplePacket("hello");
        show("User", packet);
        packet = new ApplicationLayer(packet);
        show("Application", packet);
        packet = new TransportLayer(packet);
        show("Transport", packet);
        packet = new NetworkLayer(packet);
        show("Network", packet);
        packet = new DataLinkLayer(packet);
        show("Data-link", packet);
        packet = new PhysicalLayer(packet);
        show("Physical", packet);

        // The same chain in one expression:
        // new PhysicalLayer(new DataLinkLayer(new NetworkLayer(
        //     new TransportLayer(new ApplicationLayer(new SimplePacket("hello"))))));
    }
}
