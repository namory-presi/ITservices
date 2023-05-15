# from django.db import models
# from versatileimagefield.fields import VersatileImageField, PPOIField
# import uuid
# import random
# import os
# from django.db.models import F
# from django.core.validators import MaxValueValidator, MinValueValidator
# from django.db.models import Q
# from mptt.models import MPTTModel, TreeForeignKey, TreeManager, TreeManyToManyField


# def get_filename_ext(filepath):
#     base_name = os.path.basename(filepath)
#     name, ext = os.path.splitext(base_name)
#     return name, ext


# def upload_image_path(instance, filename):
#     new_filename = random.randint(1, 3910209312)
#     name, ext = get_filename_ext(filename)
#     final_filename = f'{new_filename}{ext}'
#     return f"upload/image/{new_filename}/{final_filename}"



# class ImageExampleModel(models.Model):
#     name = models.CharField(
#         'Name',
#         max_length=80,
#         blank=True,
#         null=True
#     )
#     image = VersatileImageField(
#         'Image',
#         upload_to=upload_image_path,
#         width_field='width',
#         height_field='height',
#         ppoi_field='ppoi'
#     )
#     height = models.PositiveIntegerField(
#         'Image Height',
#         blank=True,
#         null=True
#     )
#     width = models.PositiveIntegerField(
#         'Image Width',
#         blank=True,
#         null=True
#     )
#     ppoi = PPOIField(
#         'Image PPOI'
#     )
    
    
#     class Meta:
#         verbose_name = 'Image Example'
#         verbose_name_plural = 'Image Examples'
