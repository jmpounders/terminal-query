import os
import click

from terminal_query.llm.client import get_llm_client
from terminal_query.llm.messages import UserMessage, SystemMessage
from terminal_query.llm.openaiapi import start_streaming_chat


MODEL_NAME = os.getenv('QMODEL', 'gpt-4o')


@click.command()
@click.argument('query', nargs=-1)
def main(query: tuple):
    """
    CLI application that sends user queries to an LLM and prints the response.

    Args:
        query (tuple): The user query to send to the LLM.
    """

    # Define the environment variable names for different LLM providers
    llm_api_key_env_vars = [
        'OPENAI_API_KEY',
        # 'ANTHROPIC_API_KEY'
    ]

    # Determine which API key is set
    for env_var in llm_api_key_env_vars:
        if env_var in os.environ:
            break
    else:
        print('Error: No valid LLM API key found in environment variables.')
        print(f'Please set one of the following environment variables: {list(llm_api_key_env_vars)}')
        return

    # Start the chat session
    chat = start_streaming_chat(MODEL_NAME, get_llm_client(env_var))

    # Create the initial system and user messages
    messages = [
        SystemMessage('You are a helpful assistant.'),
        UserMessage(' '.join(query))
    ]

    # Send the messages to the LLM and stream the response
    print("\nAssistant: ", end='', flush=True)
    for chunk in chat(messages):
        print(chunk, end='', flush=True)
    print()  # For a newline after the stream completes

if __name__ == '__main__':
    main()
