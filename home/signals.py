import uuid
from django.utils.text import slugify
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from home.models import CustomUser

def create_slug(instance, new_slug=None):
    slug = slugify(instance.get_full_name())
    if new_slug is not None:
        slug = new_slug
    qs = CustomUser.objects.filter(slug=slug).order_by('pk')
    exists = qs.exists()
    if exists:
        uuid_start = str(uuid.uuid1()).split("-", 1)[0] 
        new_slug = "%s-%s" %(slug, uuid_start)
        return create_slug(instance, new_slug=new_slug)

    return slug

@receiver(pre_save, sender=CustomUser)
def pre_save_slug_reciever(sender, instance, **kwargs):
    try:
        user = CustomUser.objects.get(pk=instance.pk)
        if instance.get_full_name() != user.get_full_name():
            instance.slug = create_slug(instance)
        elif not instance.slug:
            instance.slug = create_slug(instance)
    except CustomUser.DoesNotExist:
        pass
    