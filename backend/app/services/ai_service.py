import json
import logging

from app.core.settings import settings
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


class AIService:
    @staticmethod
    async def generate_incident_plan(
        description: str, logs: str | None, context: str | None
    ) -> dict:
        api_key = settings.AI_API_KEY
        # check for mock key
        if not api_key or "mock" in api_key.lower():
            return AIService._get_mock_incident_plan()

        client = AsyncOpenAI(api_key=api_key)

        system_prompt = """
        You are a Senior Site Reliability Engineer (SRE).
        Your task is to generate a structured remediation plan for a technical incident.
        
        OUTPUT FORMAT (JSON ONLY):
        {
            "steps": ["Step 1 description", "Step 2 command to run"],
            "warnings": ["Warning about data loss", "Warning about downtime"]
        }

        STYLE GUIDELINES:
        - Steps should be actionable (e.g., 'Check disk space with df -h', 'Restart nginx').
        - Warnings must highlight risks (data loss, service interruption).
        - Be direct. No filler words.
        """

        user_content = f"Incident Description: {description}\n"
        if context:
            user_content += f"System Context: {context}\n"
        if logs:
            user_content += f"Relevant Logs:\n{logs}\n"

        try:
            response = await client.chat.completions.create(
                model=settings.AI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                temperature=settings.AI_TEMPERATURE,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            if content is None:
                logger.error("AI Service Error: Received empty content from AI model.")
                raise ValueError("Received empty content from AI model.")
            logger.debug(f"AI Response: {content}")

            return json.loads(content)

        except Exception as e:
            logger.error(f"AI Service Error: {e}")
            return AIService._get_mock_incident_plan()

    @staticmethod
    def _get_mock_incident_plan() -> dict:
        logger.warning("USING MOCK AI SERVICE")

        return {
            "steps": [
                "Step 1",
                "Step 2",
                "Step 3",
            ],
            "warnings": [
                "Warning 1",
                "Warning 2",
            ],
        }
