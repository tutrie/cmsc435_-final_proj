from rest_framework import permissions
from rest_framework.request import Request
from django.db.models import Model
from rest_framework import views


class IsOwner(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it.
    
    Inherits from the default django permissions class.
    """

    def has_object_permission(self, request: Request, view: views, obj: Model) -> bool:
        """Determines if the user specified in the request is the same user that created the object obj.
        This function overwrites the default function and is automatically called by django rest framework when
        it is trying to determine permissions for a call to a view in the viewset.

        Args:
            request (Request): HTTP request object
            view (views): Not used for this custom permission but needed to define the function.
            obj (Model): Model object that we are trying to test for owner permissions

        Returns:
            [type]: [description]
        """

        if obj and obj.created_by:
            return obj.created_by == request.user
        else:
            return True
