from app.models.models import Tenants
from sqlalchemy.orm import Session
from typing import List, Optional
from app.daos.base.tenants_dao_base import BaseTenantsDao


class TenantsDao(BaseTenantsDao):
    """
    Tenants に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください