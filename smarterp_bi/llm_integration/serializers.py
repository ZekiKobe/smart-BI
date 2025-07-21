# llm_integration/serializers.py
from django.core.exceptions import ValidationError
import json

class GenerateSQLSerializer:
    def __init__(self, data):
        self.data = data
        self.errors = {}
        self.validated_data = None

    def is_valid(self):
        try:
            if not isinstance(self.data, dict):
                self.data = json.loads(self.data)
            
            # Required fields
            if 'prompt' not in self.data or not self.data['prompt'].strip():
                self.errors['prompt'] = "Prompt is required"
            if 'user_id' not in self.data:
                self.errors['user_id'] = "User ID is required"

            # Optional field
            model = self.data.get('model')
            
            if not self.errors:
                self.validated_data = {
                    'prompt': self.data['prompt'].strip(),
                    'user_id': self.data['user_id'],
                    'model': model
                }
                return True
            return False
        except json.JSONDecodeError:
            self.errors['non_field_errors'] = "Invalid JSON data"
            return False