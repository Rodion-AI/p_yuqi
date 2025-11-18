"""
create classes for neuro-writer
"""


# class core for base
class Core:

    def __init__(self, system, model, temperature, verbose):
        self.system = system
        self.model = model
        self.temperature = temperature
        self.verbose = verbose


# class writer for ai-agent
class Writer(Core):

    system_for_writer = """
    Тебя зовут Лика Воронова. Ты прекрасный писатель. У тебя великолепно получается стилизовать обычные текста в художественные.
    """
    model_for_writer = """
    gpt-5-mini-2025-08-07
    """
    temperature_for_writer = 1
    verbose_for_writer = 0

    def __init__(self, text, context, client):
        self.text = text
        self.context = context
        self.client = client

        # request method from Core
        super().__init__(
            system=self.system_for_writer,
            model=self.model_for_writer,
            temperature=self.temperature_for_writer,
            verbose=self.verbose_for_writer,
        )

    # function for activate
    async def activate(self):
        user_for_router = f"""
        Пожалуйста, ознакомся с контекстом и преобразуй полученный текст в художественный.
        Контектс: {self.context}
        Текст: {self.text}
        """
        messages = [
            {"role": "system", "content": self.system},
            {"role": "user", "content": user_for_router},
        ]

        completion = await self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=self.temperature
        )

        answer = completion.choices[0].message.content

        if self.verbose:
            print("\n writer: \n", answer)

        return answer
