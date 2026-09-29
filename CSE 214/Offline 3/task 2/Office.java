public abstract class Office {
    protected final ResultMediator resultMediator;
    protected final String name;

    public Office(ResultMediator resultMediator, String name) {
        this.resultMediator = resultMediator;
        this.name = name;
    }

    public String getName() {
        return name;
    }
}