from langchain.callbacks.base import BaseCallbackHandler
from termcolor import colored

class FullContextCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print(colored("\n=== Full Prompt (including context) ===", "green"))
        for i, prompt in enumerate(prompts):
            role = "System" if i == 0 else "Human"
            print(colored(f"\n--- {role} ---", "cyan"))
            print(colored(prompt, "green"))
        print(colored("==========================================\n", "green"))

    def on_llm_end(self, response, **kwargs):
        print(colored("\n=== AI Response ===", "green"))
        print(colored(response.generations[0][0].text, "green"))
        print(colored("====================\n", "green"))
