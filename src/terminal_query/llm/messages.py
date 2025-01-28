from dataclasses import dataclass
import json


@dataclass(frozen=True)
class ToolCall:
    tool_call_id: str
    tool_type: str
    function_name: str
    function_args: dict


@dataclass(frozen=True)
class SystemMessage:
    content: str
    role: str = 'system'


@dataclass(frozen=True)
class UserMessage:
    content: str
    role: str = 'user'


@dataclass(frozen=True)
class AssistantMessage:
    content: str
    tool_calls: list[ToolCall] | None = None
    role: str = 'assistant'


@dataclass(frozen=True)
class ToolMessage:
    content: str | None
    tool_call_id: str
    role: str = 'tool'


Message = SystemMessage | UserMessage | AssistantMessage | ToolMessage


def toolcall_to_dict(tool_call: ToolCall) -> dict:
    """Convert a ToolCall to a dict that can be embedded in an API message."""
    return {
        'id': tool_call.tool_call_id,
        'type': 'function',
        'function': {
            'name': tool_call.function_name,
            'arguments': json.dumps(tool_call.function_args)
        }
    }


def message_to_dict(message: Message) -> dict:
    """Convert a message to a dict that can be passed to the API.

    This is much, much faster than the built in dataclasses.asdict function."""

    output_dict = {}
    for key, value in vars(message).items():
        if value is None:
            continue

        # Handle lists of tools calls in messages
        if key == 'tool_calls' and value is not None:
            output_dict[key] = [toolcall_to_dict(tool_call) for tool_call in value]
        else:
            output_dict[key] = value

    return output_dict


def dict_to_message(message_dict: dict) -> Message:
    """Convert a dict to a message."""
    if message_dict['role'] == 'system':
        return SystemMessage(message_dict['content'])
    if message_dict['role'] == 'user':
        return UserMessage(message_dict['content'])
    if message_dict['role'] == 'assistant':
        if 'tool_calls' in message_dict:
            tool_calls = [
                ToolCall(
                    tool_call['id'],
                    tool_call['type'],
                    tool_call['function']['name'],
                    json.loads(tool_call['function']['arguments'])
                )
                for tool_call in message_dict['tool_calls']
            ]
        else:
            tool_calls = None
        return AssistantMessage(
            message_dict['content'],
            tool_calls
        )
    if message_dict['role'] == 'tool':
        return ToolMessage(message_dict['content'], message_dict['tool_call_id'])

    raise ValueError('Unknown message role: ' + message_dict['role'])
