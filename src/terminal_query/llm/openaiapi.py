"""
Wrappers for OpenAI API.

The following data structures very closely mirror those required by the
OpenAI API.
- `ToolCall` encapsulates tool calling parameters.  These are created by the
  assistant/LLM.
- `ToolMessage` is a message representing the response from a tool call.
- `{User|System|Assistant}Message` objects are messages with associated rules
  and contents.  `AssistantMessage` may also hold `ToolCall`s.

Example Usage:

import groundcrew.llm.openaiapi as oai

with open('openai_key_file', 'r') as f:
    openai_key = f.read().strip()

client = oai.get_openaiai_client(openai_key)


embedding_model = oai.get_embedding_model("text-embedding-ada-002", client)
e = embedding_model(['This is a test', 'This is only a test'])
print(type(e), len(e), type(e[0][0]))


def dictionary(word):
    if word=='hacktophant':
        return 'A hacker that is also a sycophant.'
    elif word=='plasopyrus':
        return 'A hard substance found on the inner lining of a platypus bill.'
    else:
        return 'I do not know!'


function_descriptions = [
    {
        'description': 'Lookup a word in the dictionary.',
        'name': 'dictionary',
        'parameters': {
            'type': 'object',
            'properties': {
                'word': {
                    'type': 'string',
                    'description': 'The word to look up.'
                },
            },
            'required': ['word']
        }
    }
]
tools = [{'type':'function', 'function':func} for func in function_descriptions]
tool_functions = {'dictionary': dictionary}

model = 'gpt-4-1106-preview'
chat = oai.start_chat(model, client)

messages = [
    oai.SystemMessage(
        'You are a helpful assistant that finds the meaning of novel words not '
        'frequently encountered in the English language.'
    ),
    oai.UserMessage('What do the words hacktophant and plasopyrus mean?')
]
response = chat(
    messages,
    tools=tools
)
messages.append(response)
print(response)

if response.tool_calls is not None:
    tool_output_messages = [
        oai.ToolMessage(
            str(tool_functions[tool.function_name](**tool.function_args)),
            tool.tool_call_id)
        for tool in response.tool_calls
    ]
    messages += tool_output_messages

response = chat(messages, tools=tools)
print(response)
"""

from typing import Callable, Any, Generator
import json

import openai

from terminal_query.llm.messages import (
    ToolCall,
    UserMessage,
    AssistantMessage,
    Message,
    message_to_dict
)


def get_openaiai_client(api_key: str | None = None, **kwargs) -> openai.Client:
    """Get an OpenAI API client."""
    return openai.OpenAI(api_key=api_key, **kwargs)


def message_from_api_response(response: dict) -> AssistantMessage:
    """Parse the API response."""
    completion = response.choices[0].message

    if completion.tool_calls is not None:
        tool_calls = [
            ToolCall(
                tool_call.id,
                tool_call.type,
                tool_call.function.name,
                json.loads(tool_call.function.arguments))
            for tool_call in completion.tool_calls
        ]
    else:
        tool_calls = None

    return AssistantMessage(completion.content, tool_calls)


def start_streaming_chat(
        model: str,
        client: openai.Client,
    ) -> Callable[[list[Message], Any], Generator[str, None, None]]:
    """Make an LLM interface function that you can use with Messages.

    This will return a function that can be called with a list of messages.
    Optional arguments to this function should conform with parameter requirements
    of the OpenAI API, e.g., `tools`, `temperature`, `seed`, etc."""

    def chat_func(messages: list[Message], *args, **kwargs):
        assert len(messages) > 0

        input_messages = [message_to_dict(message) for message in messages]
        try:
            stream = client.chat.completions.create(
                messages=input_messages,
                model=model,
                stream=True,
                *args,
                **kwargs
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        except openai.APIError as e:
            print(f'There was an API error: {e}')
            return UserMessage(f'There was an API error: {e}.  Please try again.')

    return chat_func
