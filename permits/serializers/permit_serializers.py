from rest_framework import serializers
from permits.models import Permit

class PermitSerializer(serializers.ModelSerializer):
  class Meta:
    model = Permit
    fields = ['id', 'name', 'license_plate', 'address', 'status','created_at'] 
    read_only_fields = ['status']

  def validate(self, data):
    request = self.context.get('request')
    user = request.user if request else None

    if self.context.get('validate_for') == 'permit_create':
      for field in ['name', 'license_plate', 'address']:
        if not data.get(field):
          raise serializers.ValidationError({field: "This field is required."})

      if user and data.get('name') != user.username:
        raise serializers.ValidationError({"name": "Incorrect user-name for logged in user"})
    
    return data
