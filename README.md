# Telegram Chatbot with Message Summarization

This project is a Telegram chatbot that can interact with users, maintain chat history, and provide summaries of past conversations. The bot is designed to be flexible, allowing it to operate in either a local mode or via an API, depending on the configuration.

https://github.com/user-attachments/assets/76780e14-b5db-4411-9216-0dbb6b5674bf

## Features

- **Chat History Management**: The bot keeps track of recent messages in a chat, allowing it to provide context-aware responses.
- **Message Summarization**: Users can request summaries of the last `n` messages, with options for both English and Chinese summaries.
- **Superchat Support**: The bot can handle messages in different threads within a Superchat, maintaining separate histories for each thread.
- **Customizable System Prompt**: The bot's behavior can be customized by modifying the system prompt in the configuration file.
- **Local and API Modes**: The bot can operate in two modes:
  - **API Mode** (**recommended**): Connects to an external API that supports OpenAI API (e.g., DeepSeek) for generating responses. 
  - **Local Mode**: Uses a local chatbot model (Qwen2.5-7B-Instruct) for generating responses.

## Installation

### API Mode (Recommended)

1. **Clone the Repository**:
   ```bash
   git clone git@github.com:runqiuw/context_chatbot_telegram.git
   cd telegram-chatbot
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.8 or higher installed. Then, install the required packages:
   ```bash
   pip install json
   pip install logging
   pip install python-telegram-bot --upgrade
   pip install openai
   ```

3. **Configure the Bot**:
   - Create a `config.json` file in the root directory with the following structure:
      - To begin, you need an Access Token. If you haven't got one, follow the steps [here](https://core.telegram.org/bots/tutorial). 

     ```json
     {
       "TOKEN": "YOUR_TELEGRAM_BOT_TOKEN",
       "username": "YOUR_BOT_USERNAME",
       "mode": "api",  
       "api_key": "YOUR_API_KEY", 
       "base_url": "YOUR_API_BASE_URL", 
       "model": "YOUR_MODEL_NAME",
       "context_length": 100
     }
     ```
   - Replace the placeholders with your actual bot token, username, and API details. See the `Configuration` section below for more details.

4. **Run the Bot**:
   ```bash
   python main.py
   ```

### Local Mode

1. **Clone the Repository**:
   ```bash
   git clone git@github.com:runqiuw/context_chatbot_telegram.git
   cd telegram-chatbot
   ```

2. **Install Dependencies**:
   - Ensure: 
        1. You have Python 3.8 or higher installed.
        2. You have an Nvidia GPU with at least 8GB display memory.
        3. You have installed `pytorch` that is compatible with your CUDA. If not, use `nvcc -V` to check the version of your CUDA and install the corresponding `pytorch` version from [the official website](https://pytorch.org/get-started/locally/).
        4. Your hard drive has at least 15GB of free space. 
    - Then, install the required packages:
        - If you have trouble insntalling `autoawq`, [this](https://askubuntu.com/questions/1491254/installing-cuda-on-ubuntu-23-10-libt5info-not-installable) may help.
   ```bash
   pip install json
   pip install logging
   pip install python-telegram-bot --upgrade
   pip install transformers -U
   pip install autoawq
   ```

3. **Configure the Bot**:
   - Create a `config.json` file in the root directory with the following structure:
      - To begin, you need an Access Token. If you haven't got one, follow the steps [here](https://core.telegram.org/bots/tutorial). 

     ```json
     {
       "TOKEN": "YOUR_TELEGRAM_BOT_TOKEN",
       "username": "YOUR_BOT_USERNAME",
       "mode": "local", 
       "api_key": "YOUR_API_KEY",
       "base_url": "YOUR_API_BASE_URL",  
       "model": "YOUR_MODEL_NAME",  
       "context_length": 100 
     }
     ```
   - Replace the placeholders with your actual bot token, username, and API details. See the `Configuration` section below for more details.

4. **Run the Bot**:
   ```bash
   python main.py
   ```

## Configuration

The bot's behavior can be customized by modifying the `config.json` file:

- **TOKEN**: Your Telegram bot token.
- **username**: The username of your bot.
- **mode**: Set to `"local"` to use a local chatbot model or `"api"` to use an external API.
- **api_key**: The API key for the external service (required if mode is `"api"`).
- **base_url**: The base URL for the external API (required if mode is `"api"`).
- **model**: The model name to use with the external API (required if mode is `"api"`).
- **context_length**: The maximum number of messages to store in the chat history.

## Usage

- **Start a Conversation**: Simply mention the bot in a message (e.g., `@yourbotname Hello!`), and it will respond.
- **Clear Chat History**: Use the `/new_chat` command to clear the chat history and start fresh.
- **Summarize Messages**: Use the `/summarize <number> <(optional)zh/en>` command to get a summary of the last `n` messages. You can specify the language (`zh` for Chinese, `en` for English) as an optional argument.
- **Help**: Use the `/help` command to get a list of available commands and their usage.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

1. **Fork the Repository**.
2. **Create a New Branch** (`git checkout -b feature/YourFeatureName`).
3. **Commit Your Changes** (`git commit -m 'Add some feature'`).
4. **Push to the Branch** (`git push origin feature/YourFeatureName`).
5. **Open a Pull Request**.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library for providing the tools to interact with the Telegram API.
- Special thanks to [DeepSeek](https://www.deepseek.com/) for providing the API used in this project.
- Thanks to [Qwen](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) for the open-source model Qwen2.5-7B-Instruct

Enjoy chatting with your new Telegram bot! 🚀
