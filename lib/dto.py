from db.dbutils import  clzs_to_dicts
class dto(object) :
    def c_to_ds(self, objects):
        return clzs_to_dicts(objects)

from db.dbutils import exe_query
dto.ExeQueryByClz = exe_query    