from openai import OpenAI
import json

def deepseek_get_response(api_key, base_url, model, messages, temperature=1.0, stream=False):
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        stream=stream
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    
    api_key = config["api_key"]
    base_url = config["base_url"]
    model = config["model"]

    messages = [{"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello"},]


    response_content = deepseek_get_response(api_key, base_url, model, messages)
    print(response_content)