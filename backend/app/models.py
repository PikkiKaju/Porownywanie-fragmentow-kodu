from django.db import models

class Text(models.Model):
    """
    Represents a text input.

    Attributes:
        inputText: A CharField storing the user's text input.  Limited to 30 characters.
    """
    inputText = models.CharField(max_length=30)


class File(models.Model):
    """
    Represents an uploaded file.

    Attributes:
        file: A FileField to store uploaded files.  Files are uploaded to the 'uploads/' directory.  Allows for null and blank values.
    """
    file = models.FileField(upload_to='uploads/', blank=True, null=True)

    def delete(self, *args, **kwargs):
        # Delete the file from storage
        if self.file:
            self.file.delete(save=False) 

        # Remove the database record
        super().delete(*args, **kwargs)