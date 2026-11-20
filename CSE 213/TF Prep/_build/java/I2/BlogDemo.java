// 2022-23 Q4(a), 2017-18 Q8(b) — Observer: alumni blog notifies registered users; they pull the new article
import java.util.ArrayList;
import java.util.List;

interface BlogObserver { void update(Blog blog); }
class Blog {                                               // subject (publisher)
    private final List<BlogObserver> subscribers = new ArrayList<>();
    private final List<String> articles = new ArrayList<>();
    void register(BlogObserver o)   { subscribers.add(o); }
    void unregister(BlogObserver o) { subscribers.remove(o); }
    void postArticle(String title) {
        articles.add(title);
        for (BlogObserver o : subscribers) o.update(this);  // 'a new article is posted'
    }
    String getLatestArticle() { return articles.get(articles.size() - 1); }
}
class AlumniUser implements BlogObserver {               // concrete observer
    private final String name;
    AlumniUser(String name) { this.name = name; }
    public void update(Blog blog) {
        System.out.println(name + " notified: a new article is posted");
        System.out.println(name + " reads: " + blog.getLatestArticle());   // pull model
    }
}
public class BlogDemo {
    public static void main(String[] args) {
        Blog blog = new Blog();
        AlumniUser a = new AlumniUser("Asef"), b = new AlumniUser("Nadia");
        blog.register(a); blog.register(b);
        blog.postArticle("Life after BUET");
        blog.unregister(a);
        blog.postArticle("Alumni reunion 2026");
    }
}
