package batch_22;

abstract class DepartmentVisit {
    public final void performVisit(String patientName, int visitId) {
        checkIn(patientName, visitId);
        recordVitals();
        assessment();
        treatment();
        dischargeSummary();
        System.out.println();
    }

    private void checkIn(String patientName, int visitId) {
        System.out.println("Check In patient:" + patientName + ",id:" + visitId);
    }

    private void recordVitals() {
        System.out.println("Record vitals , temp:98.6F and BP:120/80");
    }

    protected abstract void assessment();

    protected abstract void treatment();

    private void dischargeSummary() {
        System.out.println("Discharge Summary: patient discharged. Notes: " + dischargeNotes());
    }

    protected abstract String dischargeNotes();
}

class GeneralDepartment extends DepartmentVisit {
    protected void assessment() {
        System.out.println("Assessment: Doctor performs normal diagnosis");
    }

    protected void treatment() {
        System.out.println("Treatment: Prescribe standard medicine");
    }

    protected String dischargeNotes() {
        return "Standard follow-up in 2 weeks.";
    }
}

class PediatricsDepartment extends DepartmentVisit {
    protected void assessment() {
        System.out.println("Assessment: Doctor checks symptoms by ensuring child comfort level");
    }

    protected void treatment() {
        System.out.println("Treatment: Give child-safe medicine, friendly reassurance message");
    }

    protected String dischargeNotes() {
        return "Parents advised on home care.";
    }
}

class EmergencyDepartment extends DepartmentVisit {
    protected void assessment() {
        System.out.println("Assessment: Quick triage check (urgent/non-urgent)");
    }

    protected void treatment() {
        System.out.println("Treatment: Immediate emergency procedure");
    }

    protected String dischargeNotes() {
        return "Patient stabilized, refer to specialist.";
    }
}

public class HospitalVisit_Template {
    public static void main(String[] args) {
        System.out.println("=== General Department ===");
        new GeneralDepartment().performVisit("John Doe", 1001);

        System.out.println("=== Pediatrics Department ===");
        new PediatricsDepartment().performVisit("Little Timmy", 1002);

        System.out.println("=== Emergency Department ===");
        new EmergencyDepartment().performVisit("Jane Smith", 1003);
    }
}
