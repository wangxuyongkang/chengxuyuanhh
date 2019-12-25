from django.contrib import admin
from bokeapp.models import User,Token,Boke,Banner,Author_Center,comments,Category
# Register your models here.
admin.site.register(User)
admin.site.register(Token)
admin.site.register(Category)
admin.site.register(Boke)
admin.site.register(Banner)
admin.site.register(Author_Center)
admin.site.register(comments)
