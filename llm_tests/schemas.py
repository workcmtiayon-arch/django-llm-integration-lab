from pydantic import BaseModel, Field


class TaskSuggestion(BaseModel):
    title: str = Field(description="Titre court et actionnable de la tâche")
    priority: int = Field(description="Priorité de 1 (haute) à 3 (basse)")
    reason: str = Field(description="Justification brève de cette priorité")


class TaskAnalysis(BaseModel):
    suggestions: list[TaskSuggestion]
    summary: str = Field(description="Résumé en une phrase de l'analyse")
