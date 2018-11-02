import logging

from django.db import models, transaction
from django.utils.text import slugify


def thumbnail_name(instance, filename):
    import os
    from django.utils.timezone import now
    filename_base, filename_ext = os.path.splitext(filename)
    return 'thumbnail/%s%s' % (
        now().strftime("%Y%m%d%H%M%S"),
        filename_ext.lower(),
    )


class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True)
    thumbnail = models.ImageField(upload_to=thumbnail_name, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=100, default="New Post")
    body = models.TextField()
    posted_on = models.DateField(db_index=True, auto_now_add=True)
    views = models.IntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Blog, self).save(*args, **kwargs)
        self.create_blog_thumbnail()

    def create_blog_thumbnail(self):
        import os
        from PIL import Image
        from django.core.files.storage import default_storage as storage
        if not self.thumbnail:
            return ""
        file_path = self.thumbnail.name
        filename_base, filename_ext = os.path.splitext(file_path)
        thumb_file_path = "%s%s" % (filename_base, filename_ext)
        if storage.exists(thumb_file_path):
            return "exists"
        try:
            # resize the original image and return url path of the thumbnail
            f = storage.open(file_path, 'r')
            image = Image.open(f.name)
            width, height = image.size

            if width > height:
                delta = width - height
                left = int(delta / 2)
                upper = 0
                right = height + left
                lower = height
            else:
                delta = height - width
                left = 0
                upper = int(delta / 2)
                right = width
                lower = width + upper

            image = image.crop((left, upper, right, lower))
            image = image.resize((50, 50), Image.ANTIALIAS)

            f_thumb = storage.open(thumb_file_path, "w")
            image.save(f_thumb)
            f_thumb.close()
            return "success"
        except:
            logging.exception('Exception while Image processing')
            return "error"

    def get_thumbnail_url(self):
        import os
        from django.core.files.storage import default_storage as storage
        if not self.thumbnail:
            return ""
        # file_path = self.thumbnail.name
        # filename_base, filename_ext = os.path.splitext(file_path)
        # thumb_file_path = "%s%s" % (filename_base, filename_ext)
        thumb_file_path = "%s" % (self.thumbnail.name)
        if storage.exists(thumb_file_path):
            return storage.url(thumb_file_path)
        return ""

    @classmethod
    def increment_view(cls, pk):
        with transaction.atomic():
            blog = (
                cls.objects
                    .select_for_update()
                    .get(id=pk)
            )

            blog.views += 1
            blog.save()

        return blog


def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "blog_images/%s-%s" % (slug, filename)


class Images(models.Model):
    post = models.ForeignKey(Blog, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename, blank=True)

    def get_image_url(self):
        import os
        from django.core.files.storage import default_storage as storage
        if not self.image:
            return ""
        thumb_file_path = "%s" % (self.image.name)
        if storage.exists(thumb_file_path):
            return storage.url(thumb_file_path)
        return ""


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __str__(self):
        return self.title
