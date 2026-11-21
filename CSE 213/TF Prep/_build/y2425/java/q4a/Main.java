import java.util.*;

enum StorageType { LOCAL_SSD, DISTRIBUTED, BOTH }
enum NetworkType { STANDARD, HIGH_SPEED_INTERCONNECT }

/** The product: immutable, created only by its Builder, therefore always valid. */
final class ClusterConfig {
    final int nodes, cpuPerNode, ramGbPerNode;
    final boolean highMemory, gpuLibraries, authentication, encryption;
    final StorageType storage;
    final NetworkType network;
    final String os, containerRuntime;
    final List<String> accessPolicies;

    private ClusterConfig(Builder b) {
        nodes = b.nodes; cpuPerNode = b.cpuPerNode; ramGbPerNode = b.ramGbPerNode; highMemory = b.highMemory;
        storage = b.storage; network = b.network; os = b.os; containerRuntime = b.containerRuntime;
        gpuLibraries = b.gpuLibs; authentication = b.authentication; encryption = b.encryption;
        accessPolicies = List.copyOf(b.accessPolicies);
    }
    public String toString() {
        return nodes + " nodes x " + cpuPerNode + " CPU, " + ramGbPerNode + " GB" + (highMemory ? " (high-mem)" : "")
             + ", " + storage + ", " + network + ", " + os + "/" + containerRuntime + (gpuLibraries ? " +GPU" : "")
             + ", auth=" + authentication + ", enc=" + encryption + ", policies=" + accessPolicies;
    }

    static class Builder {
        private int nodes, cpuPerNode, ramGbPerNode;
        private boolean highMemory, gpuLibs, gpuNodes, storageService, authentication, encryption;
        private StorageType storage;
        private NetworkType network = NetworkType.STANDARD;
        private String os, containerRuntime;
        private final List<String> accessPolicies = new ArrayList<>();

        Builder computeNodes(int nodes, int cpuPerNode)        {
            this.nodes = nodes; this.cpuPerNode = cpuPerNode; return this; }
        Builder gpuCapableNodes()                               { this.gpuNodes = true; return this; }
        Builder memory(int ramGbPerNode, boolean highMemory)   {
            this.ramGbPerNode = ramGbPerNode; this.highMemory = highMemory; return this; }
        Builder storage(StorageType s, boolean storageService) {
            this.storage = s; this.storageService = storageService; return this; }
        Builder network(NetworkType n)                          { this.network = n; return this; }
        Builder software(String os, String runtime)             {
            this.os = os; this.containerRuntime = runtime; return this; }
        Builder gpuLibraries()                                  { this.gpuLibs = true; return this; }
        Builder security(boolean auth, boolean enc, String... policies) {
            this.authentication = auth; this.encryption = enc;
            this.accessPolicies.addAll(Arrays.asList(policies)); return this;
        }

        ClusterConfig build() {                                // the only place where validity is decided
            List<String> errors = new ArrayList<>();
            if (nodes <= 0 || cpuPerNode <= 0)          errors.add("compute nodes and CPU per node are required");
            if (ramGbPerNode <= 0)                      errors.add("RAM per node is required");
            if (storage == null)                        errors.add("a storage option is required");
            if (os == null || containerRuntime == null) errors.add("operating system and container runtime are required");
            if (!authentication)                        errors.add("user authentication is mandatory");
            if (gpuLibs && !gpuNodes)                   errors.add("GPU libraries need GPU-compatible compute nodes");
            if ((storage == StorageType.DISTRIBUTED || storage == StorageType.BOTH) && !storageService)
                errors.add("distributed storage needs the distributed-storage service");
            if (!errors.isEmpty()) throw new IllegalStateException("Invalid cluster: " + errors);
            return new ClusterConfig(this);
        }
    }
}

/** Optional director: knows the recipes, not the product's internals. */
class ClusterDirector {
    ClusterConfig machineLearning(ClusterConfig.Builder b) {
        return b.computeNodes(16, 32).gpuCapableNodes().memory(512, true).storage(StorageType.BOTH, true)
                .network(NetworkType.HIGH_SPEED_INTERCONNECT).software("Linux", "Docker").gpuLibraries()
                .security(true, true, "lab-members-only").build();
    }
    ClusterConfig dataArchive(ClusterConfig.Builder b) {
        return b.computeNodes(4, 8).memory(64, false).storage(StorageType.DISTRIBUTED, true)
                .software("Linux", "Docker").security(true, true, "read-only-for-students").build();
    }
}

public class Main {
    public static void main(String[] args) {
        ClusterDirector d = new ClusterDirector();
        System.out.println(d.machineLearning(new ClusterConfig.Builder()));
        System.out.println(d.dataArchive(new ClusterConfig.Builder()));
        try {   // invalid: GPU libraries without GPU nodes, distributed storage without the service, no authentication
            new ClusterConfig.Builder().computeNodes(2, 8).memory(32, false).storage(StorageType.DISTRIBUTED, false)
                    .software("Linux", "Docker").gpuLibraries().build();
        } catch (IllegalStateException e) { System.out.println(e.getMessage()); }
    }
}
