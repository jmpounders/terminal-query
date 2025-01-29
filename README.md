# Terminal Query

Terminal Query is a powerful CLI tool that allows you to send queries to a Large Language Model (LLM) directly from your terminal. It captures your terminal input, integrates with `tmux` panes if available, and provides intelligent responses using your preferred LLM.

> This project is heavily influenced by [`shell_sage`](https://github.com/AnswerDotAI/shell_sage). This version is a bit leaner (fewer dependencies) and written in a style closer to what I prefer.

## Installation

You can install Terminal Query using `pipx`, which allows you to install and run Python applications in isolated environments.

### Prerequisites

- Python 3.11 or higher
- [`pipx`](https://pipxproject.github.io/pipx/)

### Steps

1. **Install `pipx`** (if you haven't already):

   ```bash
   python3 -m pip install --user pipx
   python3 -m pipx ensurepath
   ```

   After running the above commands, you may need to restart your terminal or run `source ~/.bashrc` (or the equivalent for your shell) to ensure `pipx` is available.

2. **Install Terminal Query with `pipx`**:

   ```bash
   pipx install terminal-query
   ```

## Usage

Once installed, you can use Terminal Query by simply invoking the command followed by your query.

### Basic Command

```bash
terminal-query "Your question here"
```

### Examples

1. **Ask a question:**

   ```bash
   terminal-query "What is the capital of France?"
   ```

2. **Pipe input from another command:**

   ```bash
   ls -l | terminal-query "Explain these files."
   ```

3. **Use with `tmux`:**

   If you're running inside a `tmux` session, Terminal Query will automatically capture the content from your current pane to provide context for the query.

## Adding a Shell Alias for Quick Access

To make using Terminal Query even more convenient, you can add an alias to your shell configuration.

### Steps

1. **Open your shell configuration file** (`~/.bashrc`, `~/.zshrc`, etc.) in your favorite text editor.

2. **Add the following line**:

   ```bash
   alias tq='terminal-query'
   ```

3. **Save the file and reload your shell**:

   ```bash
   source ~/.bashrc
   # or for zsh
   source ~/.zshrc
   ```

4. **Now you can use `tq` instead of `terminal-query`**:

   ```bash
   tq "Explain the theory of relativity."
   ```

## Environment Variables

Terminal Query relies on certain environment variables to function correctly.

- `QMODEL`: Specifies the model name to use (default is `gpt-4o`).
- `OPENAI_API_KEY`: Your OpenAI API key for accessing the LLM.

Ensure these environment variables are set in your shell. You can add them to your shell configuration file:

```bash
export QMODEL='gpt-4o'
export OPENAI_API_KEY='your-openai-api-key'
```
