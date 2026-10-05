package batch_21_C2;

interface DatabaseQuery {
    void executeQuery(String query);
}

class SQLDatabase implements DatabaseQuery {
    @Override
    public void executeQuery(String sqlQuery) {
        System.out.println("Executing SQL query: " + sqlQuery);
    }
}

class NoSQLDatabase {
    public void runQuery(String noSQLQuery) {
        System.out.println("Executing NoSQL query: " + noSQLQuery);
    }
}

class DatabaseAdapter implements DatabaseQuery {
    protected NoSQLDatabase database;

    public DatabaseAdapter(NoSQLDatabase database) {
        this.database = database;
    }

    @Override
    public void executeQuery(String query) {
        // TODO Auto-generated method stub
        database.runQuery(query);
    }

}

public class Main {
    public static void main(String[] args) {
        DatabaseQuery sqlDb = new SQLDatabase();
        sqlDb.executeQuery("SELECT * FROM users;");

        // New NoSQL database integrated through the adapter,
        // used via the exact same DatabaseQuery interface
        DatabaseQuery noSqlDb = new DatabaseAdapter(new NoSQLDatabase());
        noSqlDb.executeQuery("{ find: 'users', filter: {} }");

        // Both can be used interchangeably wherever DatabaseQuery is expected
        DatabaseQuery[] databases = { sqlDb, noSqlDb };
        for (DatabaseQuery db : databases) {
            db.executeQuery("PING");
        }
    }
}
