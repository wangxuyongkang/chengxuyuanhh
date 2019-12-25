from django.db import models
from datetime import datetime
# Create your models here.
class User(models.Model):
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女')
    )
    name = models.CharField(max_length=32, null=True, blank=True, verbose_name='姓名')
    birthday = models.DateField(default=datetime.now, verbose_name='出生年月')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='female', verbose_name='性别')
    mobile = models.CharField(null=False, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=128, null=True, blank=True, verbose_name="邮箱")
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
class Category(models.Model):
    # 书籍分类
    name = models.CharField(max_length=56)
    add_time = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.name

class Boke(models.Model):
    title = models.CharField(max_length=125,null=True,blank=True, verbose_name='标题')
    image = models.ImageField(upload_to='media/image', verbose_name="封面图片")
    describe = models.CharField(max_length=256,null=True,blank=True, verbose_name='描述')
    # 书籍对应分类
    category = models.ForeignKey(Category)
    content = models.TextField(verbose_name='博客内容')
    give_num = models.IntegerField(verbose_name='点赞')
    author = models.CharField(max_length=125,verbose_name='博主')
    is_hot = models.BooleanField(default=False, verbose_name="是否推荐")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.title


class Banner(models.Model):
    image = models.ImageField(upload_to='media/banner', verbose_name="轮播图片")
    boke = models.ForeignKey(Boke, verbose_name='博客')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    is_view = models.BooleanField(default=False,verbose_name='是否显示')
    def __str__(self):
        return self.boke.title


class comments(models.Model):
    username = models.ForeignKey(User)
    content = models.TextField(verbose_name='评论内容')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="评论时间")
    boke_comment = models.ForeignKey(Boke)
    def __str__(self):
        return self.username.name

class Token(models.Model):
    # 跟用户关联
    user = models.OneToOneField(User)
    # 用户登陆成功后的token标识
    token = models.CharField(max_length=128)
    login_time = models.DateTimeField(default=datetime.now)

class Author_Center(models.Model):
    # 头像
    head_image = models.CharField(max_length=125)
    # 入站时间
    birthday = models.DateTimeField(default=datetime.now)
    # 关联boke表
    boke_id = models.ForeignKey(Boke)

    def __str__(self):
        return self.boke_id.author


