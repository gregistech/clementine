from classes.db_handler import db_handler, db_errors, Query

class config_handler:
    def get_default_config(key):
        return db_handler.fetch_query(Query(f"SELECT {key} FROM configs WHERE id = ?", [0]))[0][0]

    def get_config(guild_id, key):
        try:
            return db_handler.fetch_query(Query(f"SELECT {key} FROM configs WHERE id = ?", [guild_id]))[0][0]
        except db_errors.FetchNoResult:
            return config_handler.get_default_config(key)
    
    def set_config(guild_id, key, value):
        if not config_handler.is_guild_entry_exist(guild_id):
            config_handler.make_guild_entry(guild_id)
        db_handler.execute_query(Query(f"UPDATE configs SET {key} = ? WHERE id = ?", (value, guild_id)))

    def is_guild_entry_exist(guild_id):
        try:
            db_handler.fetch_query(Query("SELECT * FROM configs WHERE id = ?", [guild_id]))
            return True
        except db_errors.FetchNoResult:
            return False

    def make_guild_entry(guild_id, default_id = 0):
        default_values = list(db_handler.fetch_query(Query("SELECT * FROM configs WHERE id = ?", [default_id]))[0])
        default_values[0] = guild_id 
        db_handler.execute_query(Query("INSERT INTO configs VALUES(?,?,?,?)", default_values))
