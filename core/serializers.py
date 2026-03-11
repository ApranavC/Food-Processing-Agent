from rest_framework import serializers

class AgentQuerySerializer(serializers.Serializer):
    query = serializers.CharField(required=True, help_text="The natural language question about food processing infrastructure.")
    provider = serializers.ChoiceField(choices=["OpenAI", "Google Gemini", "Groq"], default="Groq")
    model_name = serializers.CharField(required=False, allow_null=True)
