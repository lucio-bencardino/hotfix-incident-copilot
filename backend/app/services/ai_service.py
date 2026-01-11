import json
import logging

from app.core.prompts import get_system_prompt
from app.core.settings import settings
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


class AIService:
    @staticmethod
    async def generate_incident_plan(
        description: str, logs: str | None, context: str | None, role: str | None
    ) -> dict:
        api_key = settings.AI_API_KEY

        # Check for mock key
        if not api_key or "mock" in api_key.lower():
            return AIService._get_mock_incident_plan(role)

        client = AsyncOpenAI(api_key=api_key)

        system_prompt = get_system_prompt(role)

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
                raise ValueError("Received empty content from AI model.")

            logger.info(f"AI Plan generated successfully for role: {role}")
            return json.loads(content)

        except Exception as e:
            logger.error(f"AI Service Error: {e}")
            return AIService._get_mock_incident_plan(role)

    @staticmethod
    def _get_mock_incident_plan(role: str | None) -> dict:
        logger.warning(f"USING MOCK AI SERVICE (Role: {role})")

        if role == "dev":
            return {
                "steps": [
                    "Check `package.json` for version mismatch on `axios` library.",
                    "Review recent commit history for changes in `AuthService.ts`.",
                    "Run unit tests locally with `npm test -- --grep 'Auth'` to reproduce the error.",
                    "If reproducible, implement a try-catch block around the failing call.",
                ],
                "warnings": [
                    "Hotfixing directly in production might bypass CI/CD checks.",
                    "Ensure backward compatibility with mobile clients.",
                ],
            }

        # Default DevOps/SRE
        return {
            "steps": [
                "Check pod status with `kubectl get pods -n production`.",
                "Inspect pod logs using `kubectl logs -l app=payment-service --tail=100`.",
                "Check database connection pool metrics in Grafana.",
                "If pods are crashing (OOMKilled), increase memory limits in `deployment.yaml`.",
            ],
            "warnings": [
                "Restarting the database might cause temporary downtime (approx 30s).",
                "Ensure you have a recent snapshot before applying schema changes.",
            ],
        }
