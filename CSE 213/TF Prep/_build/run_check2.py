import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_slides as c
AN, IJ, PP = c.AN, c.IJ, c.PP
plan = [
 ("Lec 1 Design Principle", os.path.join(AN, "Lec 1 - Design Principle.pdf"), 1, set()),
 ("Lec 2 Basics of Design Pattern", os.path.join(AN, "Lec 2 - Basics of Design Pattern.pdf"), 33, set()),
 ("Lec 3 Creational", os.path.join(AN, "Lec 3 - Creational Design Patterns.pdf"), 43, set()),
 ("IJ 1 Structural", os.path.join(IJ, "1 - StructuralDesignPattern.pdf"), 96, set()),
 ("IJ 2 Behavioral (no Command 168-202)", os.path.join(IJ, "2 - BehavioralDesignPattern.pdf"), 209, set(range(168, 203))),
 ("IJ 3 Misc", os.path.join(IJ, "3 - Design Pattern Misc.pdf"), 435, set()),
 ("Lec 4 class diagram", os.path.join(AN, "Lec 4 - class diagram.pdf"), 443, set()),
 ("Lec 5 class diagram-final", os.path.join(AN, "Lec 5 - class diagram-final.pdf"), 459, set()),
 ("Lec 6 ERD to class", os.path.join(AN, "Lec 6 - ERD to class.pdf"), 483, set()),
 ("Lec 7 state diagram", os.path.join(AN, "Lec 7 - state diagram.pdf"), 493, set()),
 ("Lec 8 sequence", os.path.join(AN, "Lec 8 - sequence diagram.pdf"), 522, set()),
 ("Lec 9 seq-collaboration", os.path.join(AN, "Lec 9 - seq-collaboration.pdf"), 532, set()),
 ("Lec 10 additional collaboration", os.path.join(AN, "Lec 10 - additional collaboration.pdf"), 540, set()),
 ("3 - BPMN.pptx", os.path.join(PP, "pp_3_-_BPMN.pdf"), 547, set()),
 ("Use case.pptx", os.path.join(PP, "pp_Use_case.pdf"), 581, set()),
 ("IJ 4 Process + Agile", os.path.join(IJ, "4 - Process Models and Agile Development .pdf"), 597, set()),
 ("IJ 5 Unit Testing", os.path.join(IJ, "5 - Unit Testing.pdf"), 681, set()),
 ("Lec 11 Software testing", os.path.join(AN, "Lec 11 - Software testing.pdf"), 705, set()),
 ("IJ 6 Code Reviews", os.path.join(IJ, "6 - CodeReviews.pdf"), 727, set()),
 ("IJ 7 Refactoring", os.path.join(IJ, "7 - Refactoring.pdf"), 748, set()),
 ("IJ 8 Software Ethics", os.path.join(IJ, "8 - Software Ethics.pdf"), 796, set()),
 ("IJ Software Requirement Analysis", os.path.join(IJ, "Software Requirement Analysis.pdf"), 808, set()),
 ("2 - Equivalence partitioning.pptx", os.path.join(PP, "pp_2_-_Equi.pdf"), 820, set()),
 ("1 - Coverage.pptx", os.path.join(PP, "pp_1_-_Cove.pdf"), 834, set()),
]
if __name__ == "__main__":
    n = c.check(sys.argv[1], plan)
    print("TOTAL mismatching pages:", n)
