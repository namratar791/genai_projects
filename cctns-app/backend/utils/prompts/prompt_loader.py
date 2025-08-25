from pathlib import Path
from langchain_community.document_loaders import TextLoader
from typing import Union

def load_prompt_folder(file_path: Union[str, Path]) -> str:
    """
    Load a single prompt file (e.g. .txt) using TextLoader and return its content.
    
    Args:
        file_path (str | Path): Full path to the prompt file.

    Returns:
        str: Cleaned prompt content.
    """
    try:
        base_path = Path(__file__).resolve().parent  # current file's directory
        file_path = (base_path / file_path).resolve()
        # file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {file_path}")
        
        loader = TextLoader(str(file_path))
        docs = loader.load()

        if not docs:
            raise ValueError(f"No content found in prompt file: {file_path}")

        return docs[0].page_content.strip()
    
    except Exception as e:
        print(f"🚨 Error loading prompt file '{file_path}': {e}")
        return ""



