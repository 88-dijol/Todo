from rest_framework import serializers
from work.models import User,Taskmodel

class Registration(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','password','first_name','last_name']
        read_only_feilds=['id']


    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    


class todoserializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)    #23-05 userinte id mari userinte name(string value) varanam avide --it is a response
    class Meta:
        model=Taskmodel
        fields="__all__"      #ella fieldum endavanam but read only fields onnum user enter aakaruth thaniye enter aayirikyanam
        read_only_fields=['created_date','user','completed','id']

