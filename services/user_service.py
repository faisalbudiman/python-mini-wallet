from sqlalchemy import text

class UserService:
    def __init__(self, engine):
        self.engine = engine
   
    def get_user_by_id(self, id):
        conn = self.engine.connect()
        select_user = text("""
            select id from user where id = :id limit 1
        """)
        user = conn.execute(select_user, id=id).fetchone()
        conn.close()
        if user is not None:
            return {
                'id': user[0],
            }
        else:
            return None

            
    def insert_new_user(self, id):
        conn = self.engine.connect()
        trans = conn.begin()
        try:
            insert_new_user_query = text(
                """
                    insert into user
                       values(:id)
                """
            )
            conn.execute(insert_new_user_query, 
                id=id
            )

            trans.commit()
            return {
                'id': id
            }
        except:
            trans.rollback()
            raise
        finally:
            conn.close()

