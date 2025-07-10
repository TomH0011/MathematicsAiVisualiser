class SwitchModels:

    def __init__(self):
        self.switch_model = 1  # 1 = GPT, 0 = Gemini

    @property
    def model(self):
        return "gpt-4o" if self.switch_model else "gemini"

    def switch(self):
        self.switch_model = 1 - self.switch_model
        return self.model
