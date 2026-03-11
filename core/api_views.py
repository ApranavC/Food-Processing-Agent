from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AgentQuerySerializer
from agent import run_agent_query
import os
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv(override=True)

class QueryAgentView(APIView):
    """
    API endpoint that allows users to query the AI food processing agent.
    """
    def post(self, request, *args, **kwargs):
        serializer = AgentQuerySerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data.get('query')
            provider = serializer.validated_data.get('provider')
            model_name = serializer.validated_data.get('model_name')

            # Determine API Key based on provider
            api_key = None
            if provider == "OpenAI":
                api_key = os.getenv("OPENAI_API_KEY")
            elif provider == "Google Gemini":
                api_key = os.getenv("GOOGLE_API_KEY")
            else: # Groq
                api_key = os.getenv("GROQ_API_KEY")

            if not api_key:
                return Response({
                    "error": f"API Key for {provider} not found in environment."
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Run the agent query
                result = run_agent_query(
                    query=query, 
                    provider=provider, 
                    model_name=model_name, 
                    api_key=api_key
                )
                return Response({
                    "query": query,
                    "provider": provider,
                    "model_used": model_name if model_name else "default",
                    "answer": result
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
