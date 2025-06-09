from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Union, Any
from app.daos.base.base_dao import BaseDao
from app.models.models import ApplicationSnapshot

from datetime import datetime

class ApplicationSnapshotDaoBase(BaseDao[ApplicationSnapshot]):
    """
    Data Access Object for ApplicationSnapshot.
    Provides CRUD operations and utility methods for ApplicationSnapshot table.
    """
    model = ApplicationSnapshot

    def create(
        self,
        db_session: Session,
        data: Union[ApplicationSnapshot, dict]
    ) -> ApplicationSnapshot:
        """
        Create a new ApplicationSnapshot record in the database.

        Args:
            db_session (Session): SQLAlchemy database session.
            data (Union[ApplicationSnapshot, dict]): Data to create the record. Accepts model instance or dictionary.

        Returns:
            ApplicationSnapshot: The created ApplicationSnapshot instance.

        Raises:
            RuntimeError: If the creation fails.
        """
        try:
            instance = ApplicationSnapshot(**data) if isinstance(data, dict) else data
            db_session.add(instance)
            db_session.flush()
            return instance
        except Exception as e:
            db_session.rollback()
            raise RuntimeError(f"[DAO.create] Failed to create: {e}") from e

    def delete(
        self,
        db_session: Session,
        instance: ApplicationSnapshot
    ) -> None:
        """
        Delete the specified ApplicationSnapshot instance from the database.

        Args:
            db_session (Session): SQLAlchemy database session.
            instance (ApplicationSnapshot): The instance to be deleted.

        Returns:
            None

        Raises:
            RuntimeError: If the deletion fails.
        """
        try:
            db_session.delete(instance)
            db_session.flush()
        except Exception as e:
            db_session.rollback()
            raise RuntimeError(f"[DAO.delete] Failed to delete: {e}") from e

    def get_by_key(
        self,
        db_session: Session,
        id: Optional[int]    ) -> List[ApplicationSnapshot]:
        """
        Retrieve records matching the given primary key conditions.

        Args:
            db_session (Session): SQLAlchemy database session.
            id (Optional[int]): Primary key field.

        Returns:
            List[ApplicationSnapshot]: List of matching records.
        """
        query = db_session.query(ApplicationSnapshot)
        if id is not None:
            query = query.filter(ApplicationSnapshot.id == id)
        return query.all()

    def get(
        self,
        db_session: Session,
        id: Optional[int]    ) -> Optional[ApplicationSnapshot]:
        """
        Retrieve a single record by primary key.

        Args:
            db_session (Session): SQLAlchemy database session.
            id (Optional[int]): Primary key field.

        Returns:
            Optional[ApplicationSnapshot]: The matched record, or None if not found.
        """
        result = self.get_by_key(
            db_session
, id=id        )
        return result[0] if result else None

    def get_all(
        self,
        db_session: Session,
        limit: int = 100,
        offset: int = 0
    ) -> List[ApplicationSnapshot]:
        """
        Retrieve all records with optional pagination.

        Args:
            db_session (Session): SQLAlchemy database session.
            limit (int): Maximum number of records to retrieve.
            offset (int): Starting position of the query.

        Returns:
            List[ApplicationSnapshot]: List of retrieved records.
        """
        return db_session.query(ApplicationSnapshot).limit(limit).offset(offset).all()

    def count(
        self,
        db_session: Session
    ) -> int:
        """
        Count total number of records in the table.

        Args:
            db_session (Session): SQLAlchemy database session.

        Returns:
            int: Total number of records.
        """
        return db_session.query(func.count()).select_from(ApplicationSnapshot).scalar()

    def update(
        self,
        db_session: Session,
        id: Optional[int],
        update_data: dict
    ) -> Optional[ApplicationSnapshot]:
        """
        Update a record matching the given primary key with provided data.

        Args:
            db_session (Session): SQLAlchemy database session.
            id (Optional[int]): Primary key field.
            update_data (dict): Fields to update and their new values.

        Returns:
            Optional[ApplicationSnapshot]: The updated instance, or None if not found.
        """
        results = self.get_by_key(
            db_session
, id=id        )
        instance = results[0] if results else None
        if instance:
            for key, value in update_data.items():
                setattr(instance, key, value)
            db_session.add(instance)
            db_session.flush()
        return instance