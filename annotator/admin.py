from django.contrib import admin

# Register your models here.
from .models import TokenizeCodeblockForPostsCodeBlock, Posts, CodeBlockWithTokenizeCode, RemoveTagPostsBody, \
    TokenizeRemovetagbodyForRemoveTagPostsBody

admin.site.register(TokenizeCodeblockForPostsCodeBlock)
admin.site.register(Posts)
admin.site.register(CodeBlockWithTokenizeCode)
admin.site.register(RemoveTagPostsBody)
admin.site.register(TokenizeRemovetagbodyForRemoveTagPostsBody)
