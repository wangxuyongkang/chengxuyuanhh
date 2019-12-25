from rest_framework import serializers
from bokeapp.models import User,Category,Boke,comments

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    password = serializers.CharField(
        style={"input_type": "password"}, label="密码", write_only=True
    )

    def validated_password(self, value):
        # 定义验证方法
        import re
        from rest_framework.exceptions import ValidationError
        if re.match(R'[A-Z]', value):
            # 首字母大写
            if re.match(r'[a-z]', value) and re.search(r'[0-9]', value) and len(value) > 7:
                return value
            else:
                raise ValidationError('密码格式错误')
        else:
            raise ValidationError('密码首字母必须大写')

class CategorySerializers(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='list',lookup_field='id',
        lookup_url_kwarg = 'pk'
    )

    class Meta:
        model = Category
        fields = ["id","name","url"]

class BokeListSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    url = serializers.HyperlinkedIdentityField(
        view_name='detail', lookup_field='id',
        lookup_url_kwarg='pk'
    )
    class Meta:
        model = Boke
        fields = ["id","title","image","describe","add_time","url"]

class BokedetailSeralizers(serializers.ModelSerializer):
    cotegory = serializers.CharField(source='category.name')
    # author = serializers.CharField(source='author.image')
    class Meta:
        model = Boke
        fields = ["id","title","image","cotegory","content","give_num","author"]

class CommentSeralizers(serializers.ModelSerializer):
    username = serializers.CharField(source='username.name')
    boke_comment = serializers.CharField(source='boke_comment.title')
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = comments
        fields = ["username","boke_comment","content","add_time"]