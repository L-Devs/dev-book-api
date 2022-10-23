from django.db import models

# Create your models here.

class LPostModel(models.Model):
    postId = models.BinaryField(primary_key=True,unique=True)
    userid = models.IntegerField()
    postText = models.CharField(verbose_name='post_text', max_length=480)
    dateCreated = models.DateField(verbose_name='dateCreated', null = True, blank= True)
    
    class Meta:
        db_table = "Posts"

    def __str__(self) -> str:
        return self.postText

class LCommentModel(models.Model):
    commentId = models.BinaryField(primary_key=True,unique=True)
    ownerId =  models.BinaryField()
    userid = models.IntegerField()
    postText = models.CharField(verbose_name='post_text', max_length=480)
    dateCreated = models.DateField(verbose_name='dateCreated', null = True, blank= True)

    class Meta:
        db_table = "Comments"

    def __str__(self) -> str:
        return self.postText

class LPostLikeModel(models.Model):
    likeId = models.BinaryField(primary_key=True,unique=True)
    userid = models.IntegerField()
    postId = models.BinaryField()
    isLike = models.BooleanField()
    class Meta:
        db_table = "PostLikes"

    def __str__(self) -> str:
        if self.isLike == 1:
            return "Liked"
        else:
            return "Disliked"

class LCommentLikeModel(models.Model):
    likeId = models.BinaryField(primary_key=True,unique=True)
    userid = models.IntegerField()
    commentId = models.BinaryField()
    isLike = models.BooleanField()
    class Meta:
        db_table = "CommentLikes"

    def __str__(self) -> str:
        if self.isLike == 1:
            return "Liked"
        else:
            return "Disliked"