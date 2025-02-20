import json
from pathlib import Path
from typing import Dict, List, Union

ConversationType = Dict[str, Union[str, List[Dict[str, str]]]]

class ConversationHandler:
    """
    Handles saving and loading conversation histories.
    
    Attributes:
        conv_dir: Directory path where conversation files are stored
    """
    
    def __init__(self) -> None:
        """Initialize conversation handler with storage directory."""
        self.conv_dir: Path = Path(__file__).parent / "conversations"
        self.conv_dir.mkdir(exist_ok=True)
        
    def save_conversation(self, model: str, exchanges: List[Dict[str, str]]) -> None:
        """
        Save a new conversation while maintaining only the 5 most recent ones.
        
        Args:
            model: Name of the model used in conversation
            exchanges: List of conversation exchanges containing user and BASHō messages
        """
        conversations: List[ConversationType] = []
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
            
    def get_conversations(self) -> List[ConversationType]:
        """
        Retrieve all saved conversations.
        
        Returns:
            List of conversation dictionaries containing model and exchanges
        """
        conversations: List[ConversationType] = []
        for file in sorted(self.conv_dir.glob("convo_*.json")):
            with open(file, 'r') as f:
                conversations.append(json.load(f))
        return conversations