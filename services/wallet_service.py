from sqlalchemy import text
from helper.generator_id import id_hash
from datetime import datetime

class WalletService:
    def __init__(self, engine):
        self.engine = engine

    def activate_wallet(self, user_id):
        conn = self.engine.connect()
        trans = conn.begin()
        id = id_hash()
        try:
            user_balance_query = text(
                """
                    select * from user_balance where user_id = :user_id limit 1
                """
            )
            user_balance = conn.execute(user_balance_query, user_id=user_id).fetchone()
            if user_balance:
                if user_balance["status"] == "enabled":
                    raise
                update_user_balance = text(
                    """
                        update user_balance set status = 'enabled', enabled_at=:enabled_at where user_id = :user_id
                    """
                )
                conn.execute(update_user_balance,
                    enabled_at=datetime.now(),
                    user_id=user_id
                )
                
                trans.commit()
                data = {
                    "id": user_balance["id"],
                    "owned_by": user_id,
                    "status": "enabled",
                    "enabled_at": datetime.now().isoformat()[0:-7],
                    "balance": 0
                }
                return data
            else:
                insert_user_balance = text(
                    """
                        insert into user_balance
                            (id, user_id, balance, status, enabled_at)
                        values (:id, :user_id, :balance, :status, :enabled_at)
                    """
                )
                conn.execute(insert_user_balance, 
                    id=id,
                    user_id=user_id,
                    balance=0,
                    balance_achieve=0,
                    status="enabled",
                    enabled_at=datetime.now()
                )
                data = {
                    "id": id,
                    "owned_by": user_id,
                    "status": "enabled",
                    "enabled_at": datetime.now().isoformat()[0:-7],
                    "balance": 0
                }
                trans.commit()
                return data
        except:
            trans.rollback()
            raise
        finally:
            conn.close()
    
    def my_wallet(self, user_id):
        conn = self.engine.connect()
        try:
            user_balance_query = text(
                """
                    select * from user_balance where user_id = :user_id AND status='enabled' limit 1
                """
            )
            user_balance = conn.execute(user_balance_query, user_id=user_id).fetchone()
            conn.close()
            if user_balance:
                data = {
                    "id": user_balance["id"],
                    "owned_by": user_balance["user_id"],
                    "status": user_balance["status"],
                    "enabled_at": user_balance["enabled_at"].isoformat(),
                    "balance": user_balance["balance"]
                }
                return data
            else:
                raise
        except:
            raise
        finally:
            conn.close()
        
    def deposite(self, user_id, amount, reference_id):
        conn = self.engine.connect()
        trans = conn.begin()
        id = id_hash()
        try:
            user_balance_query = text(
                """
                    select * from user_balance where user_id = :user_id AND status = 'enabled' limit 1
                """
            )
            user_balance = conn.execute(user_balance_query, user_id=user_id).fetchone()
            if user_balance:
                total_balance = user_balance["balance"]+amount

                # add transaction history
                insert_user_balance = text(
                    """
                        insert into user_balance_history
                            (id, user_balance_id, amount, reference_id, balance_before, balance_after, type)
                        values (:id, :user_balance_id, :amount, :reference_id, :balance_before, :balance_after, :type)
                    """
                )
                conn.execute(insert_user_balance, 
                    id=id,
                    user_balance_id=user_balance["id"],
                    amount=amount,
                    reference_id=reference_id,
                    balance_before=user_balance["balance"],
                    balance_after=total_balance,
                    type="credit",
                )

                # update balance user
                update_user_balance = text(
                    """
                        update user_balance set balance = :balance where user_id = :user_id
                    """
                )
                conn.execute(update_user_balance, 
                    balance=total_balance,
                    user_id=user_id,
                )

                trans.commit()
                data = {
                    "id": id,
                    "amount": amount,
                    "status": "success",
                    "deposited_at": datetime.now().isoformat()[0:-7],
                    "deposited_by": user_id,
                    "reference_id": reference_id
                }
                return data
            else:
                raise
        except:
            trans.rollback()
            raise
        finally:
            conn.close()
            
    def withdrawals(self, user_id, amount, reference_id):
        conn = self.engine.connect()
        trans = conn.begin()
        id = id_hash()
        try:
            user_balance_query = text(
                """
                    select * from user_balance where user_id = :user_id AND status = 'enabled' limit 1
                """
            )
            user_balance = conn.execute(user_balance_query, user_id=user_id).fetchone()
            if user_balance:
                if amount > user_balance["balance"]:
                    raise
                
                total_balance = user_balance["balance"]-amount

                # add transaction history
                insert_user_balance = text(
                    """
                        insert into user_balance_history
                            (id, user_balance_id, amount, reference_id, balance_before, balance_after, type)
                        values (:id, :user_balance_id, :amount, :reference_id, :balance_before, :balance_after, :type)
                    """
                )
                conn.execute(insert_user_balance, 
                    id=id,
                    user_balance_id=user_balance["id"],
                    amount=amount,
                    reference_id=reference_id,
                    balance_before=user_balance["balance"],
                    balance_after=total_balance,
                    type="debit",
                )

                # update balance user
                update_user_balance = text(
                    """
                        update user_balance set balance = :balance where user_id = :user_id
                    """
                )
                conn.execute(update_user_balance, 
                    balance=total_balance,
                    user_id=user_id,
                )

                trans.commit()
                data = {
                    "id": id,
                    "amount": amount,
                    "status": "success",
                    "withdrawn_at": datetime.now().isoformat()[0:-7],
                    "withdrawn_by": user_id,
                    "reference_id": reference_id
                }
                return data
            else:
                raise
        except:
            trans.rollback()
            raise
        finally:
            conn.close()

    def deactivate_wallet(self, user_id):
        conn = self.engine.connect()
        trans = conn.begin()
        try:
            user_balance_query = text(
                """
                    select * from user_balance where user_id = :user_id and status="enabled" limit 1
                """
            )
            user_balance = conn.execute(user_balance_query, user_id=user_id).fetchone()
            if user_balance:
                insert_user_balance = text(
                    """
                        update user_balance set status=:status, disabled_at=:disabled_at where user_id=:user_id
                    """
                )
                conn.execute(insert_user_balance, 
                    status="disabled",
                    disabled_at=datetime.now(),
                    user_id=user_id
                )
                trans.commit()
                data = {
                    "id": user_balance["id"],
                    "owned_by": user_id,
                    "status": "disabled",
                    "disabled_at": datetime.now().isoformat()[0:-7],
                    "balance": user_balance["balance"]
                }
                return data
            else:
                raise
        except:
            trans.rollback()
            raise
        finally:
            conn.close()
  