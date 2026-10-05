package claude_questions;

interface CompressionStrategy {
    int compress(String docName, int originalByte);
}

class ZipCompression implements CompressionStrategy {
    public int compress(String docName, int originalByte) {
        int saved = (int) (originalByte * 0.6);
        System.out.println(docName + " saved with ZIP. New byte: " + saved);
        return saved;
    }
}

class RARCompression implements CompressionStrategy {
    public int compress(String docName, int originalByte) {
        int saved = (int) (originalByte * 0.7);
        System.out.println(docName + " saved with RAR. New byte: " + saved);
        return saved;
    }
}

class NoCompression implements CompressionStrategy {
    public int compress(String docName, int originalByte) {
        System.out.println(docName + " saved with ZIP. New byte: 0");
        return 0;
    }
}

class SaveManager {
    private CompressionStrategy strategy;

    void setStrategy(CompressionStrategy s) {
        strategy = s;
    }

    void save(String docName, int originalByte) {
        strategy.compress(docName, originalByte);
    }
}

public class ST2_Main {
    public static void main(String[] args) {
        SaveManager mgr = new SaveManager();
        mgr.setStrategy(new ZipCompression());
        mgr.save("report.docx", 1000);
        mgr.setStrategy(new RARCompression());
        mgr.save("report.docx", 1000);
        mgr.setStrategy(new NoCompression());
        mgr.save("report.docx", 1000);
    }
}
