from config.database import DBContext


class BaseService(DBContext):
    """
    Services know, how to speak with DAO
    Service methods never return domain enitites
    """
    pass
