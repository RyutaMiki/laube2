from typing import Optional
from app.daos.base.rework_route_dao_base import ReworkRouteDaoBase
from app.models.models import ReworkRoute
from app.repositories.base.base_repository import BaseRepository

class ReworkRouteRepositoryBase(BaseRepository):
    def __init__(self, dao: Optional[ReworkRouteDaoBase] = None):
        self.dao = dao or ReworkRouteDaoBase()
    def count(self, db_session):
        return self.dao.count(db_session)
    def create(self, db_session, data):
        return self.dao.create(db_session, data)
    def delete(self, db_session, instance):
        return self.dao.delete(db_session, instance)
    def get(self, db_session, id):
        return self.dao.get(db_session, id)
    def get_all(self, db_session, limit, offset):
        return self.dao.get_all(db_session, limit, offset)
    def get_by_key(self, db_session, id):
        return self.dao.get_by_key(db_session, id)
    def insert(self, db_session, instance):
        return self.dao.insert(db_session, instance)
    def update(self, db_session, id, update_data):
        return self.dao.update(db_session, id, update_data)
