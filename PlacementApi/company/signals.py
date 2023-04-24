from django.dispatch import receiver
from django.db import models
from .models import JNF_intern_fte,JNF_placement,JNF_intern
import os


@receiver(models.signals.post_delete, sender=JNF_placement)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `JNF_placement` object is deleted.
    """
    if instance.jobDescPdf:
        if os.path.isfile(instance.jobDescPdf.path):
            os.remove(instance.jobDescPdf.path)

@receiver(models.signals.pre_save, sender=JNF_placement)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `JNF_placement` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = JNF_placement.objects.get(pk=instance.pk).jobDescPdf
    except JNF_placement.DoesNotExist:
        return False

    new_file = instance.jobDescPdf
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(models.signals.post_delete, sender=JNF_intern_fte)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `JNF_intern_fte` object is deleted.
    """
    if instance.jobDescPdf:
        if os.path.isfile(instance.jobDescPdf.path):
            os.remove(instance.jobDescPdf.path)

@receiver(models.signals.pre_save, sender=JNF_intern_fte)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `JNF_intern_fte` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = JNF_intern_fte.objects.get(pk=instance.pk).jobDescPdf
    except JNF_intern_fte.DoesNotExist:
        return False

    new_file = instance.jobDescPdf
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(models.signals.post_delete, sender=JNF_intern)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `JNF_intern` object is deleted.
    """
    if instance.jobDescPdf:
        if os.path.isfile(instance.jobDescPdf.path):
            os.remove(instance.jobDescPdf.path)

@receiver(models.signals.pre_save, sender=JNF_intern)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `JNF_intern` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = JNF_intern.objects.get(pk=instance.pk).jobDescPdf
    except JNF_intern.DoesNotExist:
        return False

    new_file = instance.jobDescPdf
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)