from classes.db_handler import db_handler, db_errors, Query

class config_handler:
    def get_default_config(key):
        return db_handler.fetch_query(Query("SELECT {field} FROM configs WHERE id = ?".format(field=key), [0]))

    def get_config(guild_id, key):
        try:
            return db_handler.fetch_query(Query("SELECT {field} FROM configs WHERE id = ?".format(field=key), [guild_id]))
        except db_errors.FetchNoResult:
            return config_handler.get_default_config(key)


