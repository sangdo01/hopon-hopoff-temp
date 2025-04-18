from rest_framework import serializers
from django.contrib.auth.models import User
from database.models import Profile
from api.ultils import format_datetime

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user model.
    """
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    date_joined = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'password', 'password2']
        read_only_fields = ['id', 'date_joined']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'is_staff': {'required': False},
            'is_superuser': {'required': False},
        }

    def get_date_joined(self, obj):
        """
        Get the date joined of the user.
        """
        return format_datetime(obj.date_joined)

    def validate(self, data):
        """
        Validate the input data.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Mật khẩu không khớp.")
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username đã tồn tại.")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email đã tồn tại.")
        return data

    def create(self, validated_data):
        """
        Create a new user.
        """
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff=validated_data.get('is_staff', False),
            is_superuser=validated_data.get('is_superuser', False),
        )
        Profile.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        """
        Update an existing user.
        """
        validated_data.pop('password2', None)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    avatar_url = serializers.ImageField(required=False, allow_null=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = [
                'id', 'phone_number', 'country', 'address', 'state', 'avatar_url', 'date_of_birth', 'gender',
                'created_at', 'updated_at', 'user', 'permissions', 'role'
            ]
        read_only_fields = ['id', 'user', 'permissions', 'role']

    def get_avatar_url(self, obj):
        """
        Get the avatar url of the user.
        """
        if obj.avatar:
            # return self.context['request'].build_absolute_uri(obj.image.url)
            return obj.avatar.url
        return None

    def get_permissions(self, obj):
        """
        Get the permissions of the user.
        """
        permissions = obj.user.user_permissions.all()
        return [permission.code for permission in permissions]
    
    def get_role(self, obj):
        """
        Get the role of the user.
        """
        try:
            return obj.user.userrole.role.name
        except AttributeError:
            return None
    
    def create(self, validated_data):
        profle = Profile.objects.create(**validated_data)
        return profle
    
    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.country = validated_data.get('country', instance.country)
        instance.address = validated_data.get('address', instance.address)
        instance.state = validated_data.get('state', instance.state)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance
        
    
    
