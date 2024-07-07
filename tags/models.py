from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# custom manager


class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return TaggedItem.objects\
            .select_related("tag")\
            .filter(
                content_type=content_type,
                object_id=obj_id
            )

# Create your models here.


class Tag(models.Model):
    lable = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.lable


class TaggedItem(models.Model):
    # use the custom manager
    objects = TaggedItemManager()
    # what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # type (product,video,article)
    # ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveSmallIntegerField()

    content_object = GenericForeignKey()
