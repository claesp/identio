DROP TABLE IF EXISTS identifier;

CREATE TABLE identifier (
  identifier_id INTEGER PRIMARY KEY AUTOINCREMENT,
  identifier_name TEXT UNIQUE NOT NULL,
  identifier_description TEXT NOT NULL,
  identifier_cluster_name TEXT NOT NULL
);

CREATE TABLE cluster (
  cluster_id INTEGER PRIMARY KEY AUTOINCREMENT,
  identifier_id INTEGER NOT NULL,
  cluster_name TEXT NOT NULL
);
