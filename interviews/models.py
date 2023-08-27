import uuid

from django.conf import settings
from django.db import models

from .services import GptService


class Chat(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=100, editable=False)
    job = models.ForeignKey("jobs.Job", on_delete=models.CASCADE, related_name="chats")
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
            self.title = f"Chat {self.job.title} - {self.uuid}"
            super().save(*args, **kwargs)
            initial_prompt = settings.INITIAL_PROMPT_TEMPLATE
            initial_prompt = initial_prompt.replace("{job_title}", self.job.title)
            initial_prompt = initial_prompt.replace("{job_requirements}", self.job.requirements)
            initial_prompt = initial_prompt.replace("{job_responsibilities}", self.job.responsibilities)
            Message.objects.create(chat=self, role="system", content=initial_prompt)
        else:
            super().save(*args, **kwargs)


class Message(models.Model):
    ROLE_CHOICES = (
        ("system", "System"),
        ("user", "Candidate"),
        ("assistant", "Interviewer")
    )

    chat = models.ForeignKey("interviews.Chat", on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} - {self.chat.title}"
    
    def save(self, *args, **kwargs):
        if not self.pk and self.role !="assistant" and not self.chat.completed:
            super().save(*args, **kwargs)

            if self.role == "user" and self.chat.messages.filter(role="assistant").count() >= 10:
                Message.objects.create(
                    chat=self.chat,
                    role="system",
                    content= "Provide candidate feedback, which should include highlighting both positive and negative aspects and explaining why. Additionally, describe areas for improvement, suggesting specific topics of hard and soft skills for further study. Also, mention whether the candidate fits the profile required for the position"
                )
                self.chat.completed = True
                self.chat.save()

            else:
                service = GptService()
                Message.objects.create(
                    chat=self.chat,
                    role="assistant",
                    content=service.get_chat_completion(self.chat.messages.all())
                )
        else:
            super().save(*args, **kwargs)