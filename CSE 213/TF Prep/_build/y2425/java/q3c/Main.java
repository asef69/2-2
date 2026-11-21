import java.util.*;

// ---------- VIOLATES the Open/Closed Principle ----------
class Rectangle { double width, height; Rectangle(double w, double h) { width = w; height = h; } }
class Circle    { double radius;        Circle(double r) { radius = r; } }

class BadAreaCalculator {
    double area(Object shape) {
        if (shape instanceof Rectangle) { Rectangle r = (Rectangle) shape; return r.width * r.height; }
        else if (shape instanceof Circle) { Circle c = (Circle) shape; return Math.PI * c.radius * c.radius; }
        throw new IllegalArgumentException("unknown shape");      // a Triangle means editing this tested method
    }
}

// ---------- FOLLOWS the Open/Closed Principle ----------
interface Shape { double area(); }
class Rect implements Shape {
    private final double w, h; Rect(double w, double h) { this.w = w; this.h = h; } public double area() { return w * h; }
}
class Circ implements Shape {
    private final double r;      Circ(double r) { this.r = r; }              public double area() { return Math.PI * r * r; }
}
class Triangle implements Shape {                                   // added later: NOTHING that exists is edited
    private final double base, height;
    Triangle(double b, double h) { base = b; height = h; }
    public double area() { return 0.5 * base * height; }
}
class AreaCalculator {
    double totalArea(List<Shape> shapes) { double t = 0; for (Shape s : shapes) t += s.area(); return t; }
}

public class Main {
    public static void main(String[] a) {
        System.out.println(new AreaCalculator().totalArea(List.of(new Rect(2, 3), new Circ(1), new Triangle(4, 5))));
    }
}
