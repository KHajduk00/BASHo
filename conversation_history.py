import json
from pathlib import Path

class ConversationHandler:
    def __init__(self):
        self.conv_dir = Path(__file__).parent / "conversations"
        self.conv_dir.mkdir(exist_ok=True)
        
    def save_conversation(self, model: str, exchanges: list):
        conversations = []
        existing_files = sorted(self.conv_dir.glob("convo_*.json"), 
                              key=lambda x: int(x.stem.split('_')[1]))
        
        for file in existing_files:
            with open(file, 'r') as f:
                conversations.append(json.load(f))
            file.unlink()
            
        conversations.append({
            "model": model,
            "exchanges": exchanges
        })
        
        if len(conversations) > 5:
            conversations = conversations[-5:]
            
        for i, convo in enumerate(conversations, 1):
            with open(self.conv_dir / f"convo_{i}.json", 'w') as f:
                json.dump(convo, f, indent=2)
            
    def get_conversations(self):
        """Returns all saved conversations"""
        conversations = []
        for file in sorted(self.conv_dir.glob("convo_*.json")):
            with open(file, 'r') as f:
                conversations.append(json.load(f))
        return conversations