public class Alert {
    private final String title;
    private final AlertCategory category;
    private final String location;
    private final String severity;
    private final String instructions;

    public Alert(String title, AlertCategory category, String location, String severity, String instructions) {
        this.title = title;
        this.category = category;
        this.location = location;
        this.severity = severity;
        this.instructions = instructions;
    }

    public String getTitle() {
        return title;
    }

    public AlertCategory getCategory() {
        return category;
    }

    public String getLocation() {
        return location;
    }

    public String getSeverity() {
        return severity;
    }

    public String getInstructions() {
        return instructions;
    }

    @Override
    public String toString() {
        return "[" + category + "] " + title +
                " | Location: " + location +
                " | Severity: " + severity +
                " | Instructions: " + instructions;
    }
}
