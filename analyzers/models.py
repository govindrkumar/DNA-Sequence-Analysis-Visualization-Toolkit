from django.db import models

# Create your models here.

class SupportTicket(models.Model):
    ISSUE_CHOICE = [
        ('dna', 'DNA Analysis'),
        ('visualisation', 'Graph Generation'),
        ('account', 'Account Access'),
        ('other', 'Other Queries')
    ]

    name = models.CharField(max_length = 100)

    issue_type = models.CharField(
        max_length = 20, choices = ISSUE_CHOICE,
        default = 'technical'
    )

    issue_detail = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.issue_type}"

