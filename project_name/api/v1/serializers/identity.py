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

    # def validate_example(self, value) for a single field
    def validate(self, data):
        """
        Throw a proper error for the client side to catch and handle
        """
        if data['age'] < data['date_joined']:
            raise serializers.ValidationError('Age is an invalid value.')
        return data

    def get_pk(self, obj):
        return obj.id

