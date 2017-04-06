from django.contrib import admin

# Register your models here.
from .models import TokenizeCodeblockForPostsCodeBlock, Posts, CodeBlockWithTokenizeCode, RemoveTagPostsBody, \
    TokenizeRemovetagbodyForRemoveTagPostsBody, SentenceType, NamedEntityAnnotation, SentenceTypeAnnotation

admin.site.register(TokenizeCodeblockForPostsCodeBlock)
admin.site.register(Posts)
admin.site.register(CodeBlockWithTokenizeCode)
admin.site.register(RemoveTagPostsBody)
admin.site.register(TokenizeRemovetagbodyForRemoveTagPostsBody)
admin.site.register(NamedEntityAnnotation)
admin.site.register(SentenceType)
admin.site.register(SentenceTypeAnnotation)
