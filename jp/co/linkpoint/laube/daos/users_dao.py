from jp.co.linkpoint.laube.daos.base.models import Users
from sqlalchemy.orm import Session
from typing import List, Optional
from jp.co.linkpoint.laube.daos.base.users_dao_base import BaseUsersDao


class UsersDao(BaseUsersDao):
    """
    Users に関するカスタムDAO処理を書く場所
    """
    pass  # 必要に応じてカスタムメソッドをここに追加してください