from typing import TypeVar, Generic, Optional

from django.db import models
from django.db.models import Model

TMODEL = TypeVar("TMODEL")


class ExtendedManager(Generic[TMODEL], models.Manager):
    """
    A manager which provides common utilities
    """

    def create(self, *args, **kwargs) -> TMODEL:
        """
        Create a new model
        """
        return super(ExtendedManager, self).create(*args, **kwargs)

    @property
    def model_class(self) -> type:
        """
        class of the model the class is currently managing
        """
        return self.model.__class__

    @property
    def MultipleObjectsReturned(self):
        return getattr(self.model_class, "MultipleObjectsReturned")

    @property
    def DoesNotExist(self):
        return getattr(self.model_class, "DoesNotExist")

    def has_at_least_one(self, **kwargs) -> bool:
        """
        Check if there is at least one model associated with the specified entry.

        :param kwargs: the same as Manager.get
        """
        try:
            self.model_class._meta._default_manager.get(**kwargs)
            return True
        except self.DoesNotExist:
            return False
        except self.MultipleObjectsReturned:
            return True

    def has_at_most_one(self, **kwargs) -> bool:
        """
        Check if there is at least one model associated with the specified entry.

        :param kwargs: the same as Manager.get
        """
        try:
            self.model_class._meta._default_manager.get(**kwargs)
            return True
        except self.DoesNotExist:
            return True
        except self.MultipleObjectsReturned:
            return False

    def has_exactly_one(self, **kwargs) -> bool:
        """
        Check if there is exactly one model associated with the specified entry.

        :param kwargs: the same as Manager.get
        """
        try:
            self.model_class._meta._default_manager.get(**kwargs)
            return True
        except self.DoesNotExist:
            return False
        except self.MultipleObjectsReturned:
            return False

    def find_only_or_fail(self, **kwargs) -> TMODEL:
        """
        Find the only one element in the model. Raises exception if either zero or more items are fetched isntead


        """
        return self.model_class._meta._default_manager.get(**kwargs)

    def find_only_or_None(self, **kwargs) -> Optional[TMODEL]:
        try:
            return self.model_class._meta._default_manager.get(**kwargs)
        except self.DoesNotExist:
            return None



