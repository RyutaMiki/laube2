from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Union, Any
from app.daos.base.base_dao import BaseDao
from app.models.models import ApplicationFormFormat

from datetime import datetime

class ApplicationFormFormatDaoBase(BaseDao[ApplicationFormFormat]):
    """
    Data Access Object for ApplicationFormFormat.
    Provides CRUD operations and utility methods for ApplicationFormFormat table.
    """
    model = ApplicationFormFormat

    def create(
        self,
        db_session: Session,
        data: Union[ApplicationFormFormat, dict]
    ) -> ApplicationFormFormat:
        """
        Create a new ApplicationFormFormat record in the database.

        Args:
            db_session (Session): SQLAlchemy database session.
            data (Union[ApplicationFormFormat, dict]): Data to create the record. Accepts model instance or dictionary.

        Returns:
            ApplicationFormFormat: The created ApplicationFormFormat instance.

        Raises:
            RuntimeError: If the creation fails.
        """
        try:
            instance = ApplicationFormFormat(**data) if isinstance(data, dict) else data
            db_session.add(instance)
            db_session.flush()
            return instance
        except Exception as e:
            db_session.rollback()
            raise RuntimeError(f"[DAO.create] Failed to create: {e}") from e

    def delete(
        self,
        db_session: Session,
        instance: ApplicationFormFormat
    ) -> None:
        """
        Delete the specified ApplicationFormFormat instance from the database.

        Args:
            db_session (Session): SQLAlchemy database session.
            instance (ApplicationFormFormat): The instance to be deleted.

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
        id: Optional[int]    ) -> List[ApplicationFormFormat]:
        """
        Retrieve records matching the given primary key conditions.

        Args:
            db_session (Session): SQLAlchemy database session.
            id (Optional[int]): Primary key field.

        Returns:
            List[ApplicationFormFormat]: List of matching records.
        """
        query = db_session.query(ApplicationFormFormat)
        if id is not None:
            query = query.filter(ApplicationFormFormat.id == id)
        return query.all()

    def get(
        self,
        db_session: Session,
        id: Optional[int]    ) -> Optional[ApplicationFormFormat]:
        """
        Retrieve a single record by primary key.

        Args:
            db_session (Session): SQLAlchemy database session.
            id (Optional[int]): Primary key field.

        Returns:
            Optional[ApplicationFormFormat]: The matched record, or None if not found.
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
    ) -> List[ApplicationFormFormat]:
        """
        Retrieve all records with optional pagination.

        Args:
            db_session (Session): SQLAlchemy database session.
            limit (int): Maximum number of records to retrieve.
            offset (int): Starting position of the query.

        Returns:
            List[ApplicationFormFormat]: List of retrieved records.
        """
        return db_session.query(ApplicationFormFormat).limit(limit).offset(offset).all()

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
        return db_session.query(func.count()).select_from(ApplicationFormFormat).scalar()

    def update(
        self,
        db_session: Session,
        id: Optional[int],
        update_data: dict
    ) -> Optional[ApplicationFormFormat]:
        """
        Update a record matching the given primary key with provided data.

        Args:
            db_session (Session): SQLAlchemy database session.
            id (Optional[int]): Primary key field.
            update_data (dict): Fields to update and their new values.

        Returns:
            Optional[ApplicationFormFormat]: The updated instance, or None if not found.
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