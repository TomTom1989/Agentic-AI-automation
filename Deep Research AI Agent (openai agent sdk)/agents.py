import uuid
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union, get_origin, get_args
from pydantic import BaseModel
from functools import wraps
import os
import openai
import json

T = TypeVar('T', bound=BaseModel)

def function_tool(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Dict[str, Any]:
        result = await func(*args, **kwargs)
        return result
    return wrapper

class ModelSettings(BaseModel):
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000
    tool_choice: Optional[str] = None

class WebSearchTool(BaseModel):
    search_context_size: str = "medium"

class Runner:
    @staticmethod
    async def run(agent: 'Agent', message: str, context: Optional[Dict] = None) -> 'AgentResponse':
        response = await agent.process(message, context or {})
        return response

def gen_trace_id() -> str:
    return str(uuid.uuid4())

class trace:
    def __init__(self, name: str, trace_id: Optional[str] = None):
        self.name = name
        self.trace_id = trace_id or gen_trace_id()

    def __enter__(self):
        print(f"Starting trace: {self.name} (ID: {self.trace_id})")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Ending trace: {self.name} (ID: {self.trace_id})")

class AgentResponse:
    def __init__(self, final_output: Any):
        self.final_output = final_output

    def final_output_as(self, output_type: Type[T]) -> T:
        if isinstance(self.final_output, output_type):
            return self.final_output
        if isinstance(self.final_output, dict):
            if hasattr(output_type, "model_fields"):
                for field_name, field in output_type.model_fields.items():
                    if field_name in self.final_output and isinstance(self.final_output[field_name], list):
                        field_type = field.annotation
                        if hasattr(field_type, "__origin__") and field_type.__origin__ is list:
                            item_type = field_type.__args__[0]
                            if issubclass(item_type, BaseModel):
                                self.final_output[field_name] = [
                                    item_type(**item) if isinstance(item, dict) else item
                                    for item in self.final_output[field_name]
                                ]
            return output_type(**self.final_output)
        return output_type(self.final_output)

class Agent:
    def __init__(
        self,
        name: str,
        instructions: str,
        tools: Optional[List[Callable]] = None,
        handoffs: Optional[List['Agent']] = None,
        model: str = "gpt-4",
        output_type: Optional[Type[BaseModel]] = None,
        handoff_description: Optional[str] = None,
        model_settings: Optional[ModelSettings] = None
    ):
        self.name = name
        self.instructions = instructions
        self.tools = tools or []
        self.handoffs = handoffs or []
        self.model = model
        self.output_type = output_type
        self.handoff_description = handoff_description
        self.model_settings = model_settings

    async def process(self, message: str, context: Dict) -> AgentResponse:
        import asyncio
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            client = openai.OpenAI(api_key=api_key)
            messages = [
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": message}
            ]
            def call_openai():
                return client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                )
            response = await asyncio.to_thread(call_openai)
            reply = response.choices[0].message.content
            # Try to parse as JSON if output_type is set
            if self.output_type:
                try:
                    data = json.loads(reply)
                    return AgentResponse(data)
                except Exception:
                    pass  # fallback to plain message
            return AgentResponse({"message": reply})
        # Fallback to mock if no API key
        if self.output_type and hasattr(self.output_type, "model_fields"):
            mock_data = {}
            for field_name, field in self.output_type.model_fields.items():
                field_type = field.annotation
                origin = get_origin(field_type)
                if origin is list:
                    item_type = get_args(field_type)[0]
                    if issubclass(item_type, BaseModel):
                        mock_item = {}
                        for item_field_name, item_field in item_type.model_fields.items():
                            if get_origin(item_field.annotation) is list:
                                mock_item[item_field_name] = []
                            else:
                                mock_item[item_field_name] = f"Mock {item_field_name}"
                        mock_data[field_name] = [mock_item]
                    else:
                        mock_data[field_name] = []
                else:
                    if field_type == str:
                        mock_data[field_name] = f"Mock {field_name}"
                    elif field_type == int:
                        mock_data[field_name] = 0
                    elif field_type == float:
                        mock_data[field_name] = 0.0
                    elif field_type == bool:
                        mock_data[field_name] = False
                    else:
                        mock_data[field_name] = None
            return AgentResponse(mock_data)
        return AgentResponse({"message": f"Processed by {self.name}: {message}"})

    def as_tool(self, tool_name: str, tool_description: str) -> Callable:
        async def tool_func(*args, **kwargs) -> Dict:
            response = await self.process(str(args) + str(kwargs), {})
            return response.final_output
        return tool_func 