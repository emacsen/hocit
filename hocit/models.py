from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from markupfield.fields import MarkupField
import uuid


class Actor(models.Model):
    """The Reporer is someone who submits a report to us.

    All fields are essentially optional
    """
    name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    phone_number = PhoneNumberField(blank=True)
    notes = MarkupField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True)


class Report(models.Model):
    """A Report is a discussion about an incident.

    It should (hopefully) only discuss one incident. It consists of a
    series of Notes
    """
    # UUID is used because we may (in the future) make these reports
    # viewable outside the app, by UUID so they're not guessable
    id = models.UUIDField(default=uuid.uuid4, primary_key=True,
                          editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reporter = models.ForeignKey(Actor, on_delete=models.CASCADE,
                                 related_name='reports')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE,
                                    blank=True)
    overview = MarkupField()


def note_file_path(instance, filename):
    # The file will be uploaded to MEDIA/note_id/<filename>
    #
    # This makes a lot of directories, but it keeps original filenames
    # in tact
    return 'report_{0}/{1}'.format(instance.note.id, filename)


class Note(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Actor, on_delete=models.CASCADE,
                               related_name='all_notes')
    report = models.ForeignKey(Report, on_delete=models.CASCADE,
                               related_name='notes')
    body = MarkupField()
    # We could have multiple files per note, but this would be a lot
    # more complicated than just one per note. We can simply attach
    # some text saying that if you need more than one file, make a new
    # note.
    attached_file = models.FileField(upload_to=note_file_path)
