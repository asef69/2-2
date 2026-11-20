// Minimal stand-ins for JUnit 4 so the test classes compile and run without the JUnit jar (not part of the notes)
package org.junit;
import java.lang.annotation.*;
@Retention(RetentionPolicy.RUNTIME) @Target(ElementType.METHOD)
public @interface Test { Class<? extends Throwable> expected() default None.class; class None extends Throwable { } }
