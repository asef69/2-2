package a1_23_abstract;

import org.w3c.dom.Text;

interface Button {
    void render();
}

interface TextField {
    void render();
}

interface DialogBox {
    void render();
}

class LightButton implements Button {
    @Override
    public void render() {
        System.out.println("Light Button");
    }
}

class DarkButton implements Button {
    @Override
    public void render() {
        System.out.println("Dark Button");
    }
}

class LightTextField implements TextField {
    @Override
    public void render() {
        System.out.println("Light Text Field");
    }
}

class DarkTextField implements TextField {
    @Override
    public void render() {
        System.out.println("Dark Text Field");
    }
}

class LightDialogBox implements DialogBox {
    @Override
    public void render() {
        System.out.println("Light Dialog Box");
    }
}

class DarkDialogBox implements DialogBox {
    @Override
    public void render() {
        System.out.println("Dark Dialog Box");
    }
}

interface ThemeFactory {
    TextField createText();

    DialogBox createDialog();

    Button createButton();
}

class LightFactory implements ThemeFactory {
    @Override
    public TextField createText() {
        return new LightTextField();
    }

    @Override
    public Button createButton() {
        return new LightButton();
    }

    @Override
    public DialogBox createDialog() {
        return new LightDialogBox();
    }
}

class DarkFactory implements ThemeFactory {
    @Override
    public TextField createText() {
        return new DarkTextField();
    }

    @Override
    public Button createButton() {
        return new DarkButton();
    }

    @Override
    public DialogBox createDialog() {
        return new DarkDialogBox();
    }
}

class Application {
    private Button button;
    private TextField textField;
    private DialogBox dialogBox;

    public Application(ThemeFactory themeFactory) {
        button = themeFactory.createButton();
        textField = themeFactory.createText();
        dialogBox = themeFactory.createDialog();
    }

    public void renderTheme() {
        button.render();
        dialogBox.render();
        textField.render();
    }
}

public class Main {
    public static void main(String[] args) {
        ThemeFactory factory = new LightFactory();
        Application app = new Application(factory);
        app.renderTheme();
        System.out.println("================================");
        ThemeFactory newFactory = new DarkFactory();
        Application app2 = new Application(newFactory);
        app2.renderTheme();

    }
}
