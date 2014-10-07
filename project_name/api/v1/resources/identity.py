from rest_framework import viewsets
from {{ project_name }}.apps.identity import models
from {{ project_name }}.api.v1.serializers.identity import IdentitySerializer


class Identity(viewsets.ModelViewSet):
    """
    List all identities
    """
    queryset = models.Identity.objects.all()
    serializer_class = IdentitySerializer

