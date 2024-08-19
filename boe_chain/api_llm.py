from langchain_core.language_models.chat_models import BaseChatModel
class APILLM(BaseChatModel):
    def __init__(self, model_index):
        super().__init__()
        self.model_index = model_index
        