# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class CodeBlockWithTokenizeCode(models.Model):
    SMALL_CODE_BLOCK = 0
    LARGE_CODE_BLOCK = 1
    CODE_BLOCK_TYPE = (
        (SMALL_CODE_BLOCK, "small code block"),
        (LARGE_CODE_BLOCK, "large code block")
    )
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    parent_id = models.IntegerField(db_column='ParentId')  # Field name made lowercase.
    type = models.IntegerField(choices=CODE_BLOCK_TYPE, default=SMALL_CODE_BLOCK)
    code_block_name = models.TextField(db_column='codeBlockName', blank=True, null=True)  # Field name made lowercase.
    code_block = models.TextField(db_column='codeBlock', blank=True, null=True)  # Field name made lowercase.
    tokenize_text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'code_block_with_tokenize_code'


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Posts(models.Model):
    body = models.TextField(db_column='Body', blank=True, null=True)  # Field name made lowercase.
    viewcount = models.IntegerField(db_column='ViewCount', blank=True, null=True)  # Field name made lowercase.
    lasteditordisplayname = models.TextField(db_column='LastEditorDisplayName', blank=True,
                                             null=True)  # Field name made lowercase.
    closeddate = models.DateTimeField(db_column='ClosedDate', blank=True, null=True)  # Field name made lowercase.
    title = models.TextField(db_column='Title', blank=True, null=True)  # Field name made lowercase.
    lasteditoruserid = models.IntegerField(db_column='LastEditorUserId', blank=True,
                                           null=True)  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentID', blank=True, null=True)  # Field name made lowercase.
    lasteditdate = models.DateTimeField(db_column='LastEditDate', blank=True, null=True)  # Field name made lowercase.
    commentcount = models.IntegerField(db_column='CommentCount', blank=True, null=True)  # Field name made lowercase.
    communityowneddate = models.DateTimeField(db_column='CommunityOwnedDate', blank=True,
                                              null=True)  # Field name made lowercase.
    answercount = models.IntegerField(db_column='AnswerCount', blank=True, null=True)  # Field name made lowercase.
    acceptedanswerid = models.IntegerField(db_column='AcceptedAnswerId', blank=True,
                                           null=True)  # Field name made lowercase.
    score = models.IntegerField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    ownerdisplayname = models.TextField(db_column='OwnerDisplayName', blank=True,
                                        null=True)  # Field name made lowercase.
    posttypeid = models.IntegerField(db_column='PostTypeId', blank=True, null=True)  # Field name made lowercase.
    owneruserid = models.IntegerField(db_column='OwnerUserId', blank=True, null=True)  # Field name made lowercase.
    tags = models.TextField(db_column='Tags', blank=True, null=True)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='CreationDate', blank=True, null=True)  # Field name made lowercase.
    favoritecount = models.IntegerField(db_column='FavoriteCount', blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(db_column='Id', unique=True, primary_key=True)  # Field name made lowercase.
    lastactivitydate = models.DateTimeField(db_column='LastActivityDate', blank=True,
                                            null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'posts'


class RemoveTagPostsBody(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    removetagbody = models.TextField(db_column='RemoveTagBody', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'remove_tag_posts_body'


class TokenizeRemovetagbodyForRemoveTagPostsBody(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    tokenize_text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tokenize_RemoveTagBody_for_remove_tag_posts_body'


class TokenizeCodeblockForPostsCodeBlock(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    tokenize_text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tokenize_codeBlock_for_posts_code_block'
