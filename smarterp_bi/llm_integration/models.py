from django.db import models

class LLMProvider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    base_url = models.URLField()
    api_key = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class QueryHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    natural_language_query = models.TextField()
    generated_sql = models.TextField()
    llm_provider = models.ForeignKey(LLMProvider, on_delete=models.CASCADE)
    execution_time_ms = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    result_count = models.IntegerField(null=True)