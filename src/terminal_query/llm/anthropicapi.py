from typing import Callable

from anthropic import Anthropic

from terminal_query.llm.messages import (
    UserMessage,
    AssistantMessage,
    Message,
    message_to_dict
)


def get_anthropic_client(api_key: str) -> Anthropic:
    """Get an Anthropic API client."""
    return Anthropic(api_key=api_key)


def start_chat(model_name: str, api_client: Anthropic) -> Callable[[list[Message]], AssistantMessage]:
    """Start a chat with the API."""

    def chat_func(messages: list[Message], **kwargs) -> AssistantMessage:
        """Send messages to the API."""
        assert len(messages) > 0, 'messages must not be empty'
        try:
            response = api_client.messages.create(
                model=model_name,
                max_tokens=2048,
                messages=[message_to_dict(message) for message in messages],
                **kwargs
            )
            return AssistantMessage(response.content)
        except Exception as e:
            print(f'There was an error: {e}')
            return UserMessage(f'There was an API error: {e}.  Please try again.')

    return chat_func
