import os
from mutagen import File
from uuid import uuid4
from operator import attrgetter


from django.utils.deconstruct import deconstructible
from django.db.models import FileField
from django.core.validators import FileExtensionValidator


IMAGE_EXTS = {'png', 'jpg', 'jpeg', 'gif'}
AUDIO_EXTS = {'mp3', 'ogg', 'wav', }
VIDEO_EXTS = {'mp4', 'mkv', 'avi', 'mov',
              'wmv', 'flv', 'webm', }
DOC_EXTS = {'doc', 'docx', 'txt', 'pdf', 'rtf', 'odt', 'ott', 'xls',
            'xlsx', 'csv', 'ppt', 'pptx', 'odp', 'ods',
            'html', 'htm', 'xml'}


FILE_TYPES = {'image': IMAGE_EXTS, 'audio': AUDIO_EXTS,
              'video': VIDEO_EXTS, 'doc': DOC_EXTS}

FILE_VALIDATOR = FileExtensionValidator(IMAGE_EXTS | AUDIO_EXTS | VIDEO_EXTS)


def get_file_type(ext: str):
    ext = ext.lstrip('.').lower()
    for k, v in FILE_TYPES.items():
        if ext in v:
            return k


def set_metadata(instance):
    file = instance.file
    metadata = {'file_name': file.name,
                'size': file.size}
    ext = os.path.splitext(file.name)[-1][1:]

    if ext in AUDIO_EXTS:
        author = title = duration = None
        try:
            audio = File(file.open('rb'), easy=True)
            duration = audio.info.length
            tags = audio.tags
            title = tags.get('title', [None])[0]
            author = (tags.get('artist') or tags.get('author') or [None])[0]
        except Exception as e:
            print(e)
        metadata.update(
            {'title': title, 'author': author, 'duration': duration})
    instance.metadata = metadata


def delete_file(file: FileField):
    if file and os.path.isfile(file.path):
        os.remove(file.path)


def delete_old_file(model, instance, file_field: str = 'file'):
    try:
        old_file = getattr(model.objects.get(pk=instance.pk), file_field)
        new_file = getattr(instance, file_field)
    except:
        return
    if new_file != old_file:
        delete_file(old_file)


def msg_file_change(sender, instance):
    if not instance.pk:
        set_metadata(instance)
    delete_old_file(sender, instance)


@deconstructible
class MessageFilePath:

    def __init__(self, prefix: str, dot_path: str):
        self.prefix = prefix
        self.dot_path = dot_path

    def __call__(self, instance, fname: str) -> str:
        ext = os.path.splitext(fname)[-1]
        f_type = instance.file_type
        name = uuid4().hex
        return f"{self.prefix}/{attrgetter(self.dot_path)(instance)}/{f_type}s/{name}{ext}"
