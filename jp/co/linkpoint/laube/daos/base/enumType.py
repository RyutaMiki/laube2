from __future__ import annotations

from enum import Enum
from typing import Any, Optional, Type, TypeVar

from sqlalchemy import Integer
from sqlalchemy.types import TypeDecorator

E = TypeVar("E", bound=Enum)


class EnumType(TypeDecorator):
    """
    SQLAlchemy type decorator that stores an :class:`enum.Enum` **as an INTEGER**
    in the database while exposing the original Enum instance in Python code.

    Parameters
    ----------
    enum_class : Type[E]
        The Enum subclass this column should serialize / deserialize.

    Examples
    --------
    >>> from enum import Enum
    >>> from sqlalchemy import Column
    >>>
    >>> class Status(Enum):
    ...     ACTIVE = 1
    ...     SUSPENDED = 2
    ...
    >>> status = Column(EnumType(enum_class=Status), nullable=False, default=Status.ACTIVE)

    Notes
    -----
    * `impl` is set to :class:`sqlalchemy.Integer` so the actual column type on the DB
      side is a plain INT.
    * `cache_ok = True` tells SQLAlchemy it’s safe to cache this type object.
    """

    impl = Integer
    cache_ok = True

    def __init__(self, *, enum_class: Type[E], **kwargs: Any) -> None:
        """
        EnumTypeの初期化。

        Args:
            enum_class (Type[E]): 利用するEnumクラス
            **kwargs: TypeDecoratorへの追加パラメータ

        Raises:
            TypeError: enum_classがEnumのサブクラスでない場合に例外
        """
        if not (isinstance(enum_class, type) and issubclass(enum_class, Enum)):
            raise TypeError("enum_class must be a subclass of enum.Enum")
        self.enum_class: Type[E] = enum_class
        super().__init__(**kwargs)

    def process_bind_param(self, value: Optional[E], dialect) -> Optional[int]:
        """
        Enum値（Python側）をDB格納用の整数値に変換する。

        Args:
            value (Optional[E]): Enum値（Noneの場合はそのままNone）
            dialect: SQLAlchemy Dialect（未使用）

        Returns:
            Optional[int]: DBに書き込む整数値（またはNone）

        Raises:
            TypeError: valueがenum_class型でない場合
        """
        if value is None:
            return None
        if not isinstance(value, self.enum_class):
            raise TypeError(f"Expected {self.enum_class.__name__}, got {type(value).__name__}")
        return int(value.value)

    def process_result_value(self, value: Optional[int], dialect) -> Optional[E]:
        """
        DBから取得した整数値をEnum値（Python）に変換する。

        Args:
            value (Optional[int]): DBから返された整数値（またはNone）
            dialect: SQLAlchemy Dialect（未使用）

        Returns:
            Optional[E]: Enum値（またはNone）

        Raises:
            TypeError: valueがint型でない場合
            ValueError: valueがenum_classに該当しない場合
        """
        if value is None:
            return None
        if not isinstance(value, int):
            raise TypeError(f"Expected int from database, got {type(value).__name__}")
        try:
            return self.enum_class(value)  # type: ignore[return-value]
        except ValueError as exc:
            raise ValueError(
                f"{value!r} is not a valid value for {self.enum_class.__name__}"
            ) from exc

    def __repr__(self) -> str:
        """
        デバッグ用のrepr（列挙体クラス名を表示）。

        Returns:
            str: EnumType(class名)
        """
        return f"EnumType({self.enum_class.__name__})"
