class GenAIEvaluator:
    def __init__(self, model, human_prompt: str):
        self.model = model
        self.human_prompt = human_prompt

    def evaluate(self, input_variables: dict[str, str]) -> str:
        formatted_prompt = self.human_prompt.format(**input_variables)
        response = self.model.generate_content(formatted_prompt, generation_config={"temperature": 0})
        return response.text