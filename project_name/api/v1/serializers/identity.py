from rest_framework import serializers
from {{ project_name }}.apps.identity.models import Identity


class IdentitySerializer(serializers.ModelSerializer):
    """
    Serialize identity models
    """
    pk = serializers.SerializerMethodField()

    class Meta:
        model = Identity
        fields = ('id', 'pk', 'first_name', 'last_name', 'date_joined',)

    def validate_example(self, attrs, source):
        """
        Add custom validation for a field called "example" and throw
        a proper error for the client side to catch and handle
        """
        if not attrs['example']:
            raise serializers.ValidationError('The example field is required')
        return attrs

    def get_pk(self, obj):
        return obj.id

