from transformers import pipeline

class Chatbot:
    def __init__(self, model_name="Qwen/Qwen2.5-7B-Instruct-AWQ", 
                 system_prompt = "You are a helpful assistant, but you only answers questions that mentions you."):
        self.pipe = pipeline(
            "text-generation",  
            model=model_name,  
            device_map="auto", 
        )
        self.messages = [
            {"role": "system", "content": system_prompt},
        ]

    def extract_generated_text(self, full_response):
        assistant_start_marker = "<|im_start|>assistant"
        assistant_end_marker = "<|im_end|>"
        last_start_index = full_response.rfind(assistant_start_marker)
        if last_start_index != -1:
            generated_part = full_response[last_start_index + len(assistant_start_marker):]
            end_index = generated_part.find(assistant_end_marker)
            if end_index != -1:
                generated_part = generated_part[:end_index]
            generated_part = generated_part.strip()
            return generated_part
        else:
            return full_response

    def generate_response(self, messages):
        try:
            text = self.pipe.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )

            response = self.pipe(
                text,
                max_new_tokens=512, 
                temperature=0.7, 
            )
            return self.extract_generated_text(response[0]['generated_text'])
        except Exception as e:
            return f"An error occurred while generating the response: {str(e)}"
        
    def clear_messages(self, system_prompt):
        self.messages = [
            {"role": "system", "content": system_prompt},
        ]

    def chat(self):
        print("Welcome to the Qwen QA Bot! Type 'exit' or 'quit' to end the conversation.")
        while True:
            try:
                user_input = input("You: ")
                if user_input.lower() in ["exit", "quit"]:
                    print("Bot: Goodbye!")
                    break
                self.messages.append({"role": "user", "content": user_input})
                response = self.generate_response(self.messages)
                self.messages.append({"role": "assistant", "content": response})
                print(f"Qwen: {response}")
            except KeyboardInterrupt:
                print("\nQwen: Goodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    bot = Chatbot()
    bot.chat()