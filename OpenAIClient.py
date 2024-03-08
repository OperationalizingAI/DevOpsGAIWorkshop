from openai import OpenAI

class OpenAIClient():
    def __init__(self, api_key) -> None:
        self.client = OpenAI(
            api_key= api_key,  # defaults to os.environ.get("OPENAI_API_KEY")
        )
        # print ("OpenAI Client initialized!")


    def chat (self, messages, model="gpt-3.5-turbo"):
        chat_completion = self.client.chat.completions.create(
                        messages=messages, model=model,)
        return chat_completion

    def get_embedding(self, text: str,  model="text-embedding-ada-002") -> list[float]:
        text = text.replace("\n", " ")
        resp = self.client.embeddings.create (
            input=[text],
            model=model  )

        return resp.data[0].embedding
