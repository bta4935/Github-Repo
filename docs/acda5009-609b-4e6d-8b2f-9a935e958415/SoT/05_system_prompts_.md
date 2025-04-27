# Chapter 5: System Prompts

In the [previous chapter](04_context_initialization___formatting_.md), we saw how SoT's `get_initialized_context` method cleverly packages everything together – rules, examples, and your question – to guide the Language Model (LLM). It's like setting up the classroom perfectly for a specific lesson.

But what exactly are those "rules" or "posters on the wall"? How do we tell the LLM *precisely* how it should think using, say, Conceptual Chaining versus Chunked Symbolism? This is where **System Prompts** come into play.

## The Recipe Cards for Reasoning

Imagine the LLM is a talented, versatile chef. It can cook almost anything! But to make a specific dish perfectly, it needs a detailed recipe card.

**System Prompts** are like those recipe cards for the LLM chef. Each prompt is a detailed set of instructions specifically designed for one [Reasoning Paradigm](01_reasoning_paradigms_.md) (like Conceptual Chaining, Chunked Symbolism, or Expert Lexicons).

Just like a recipe card tells the chef:

*   **The Goal:** What dish are we making? (e.g., "Make a concise symbolic breakdown")
*   **The Ingredients:** What tools or concepts are needed? (e.g., "Use variables and equations")
*   **The Steps:** How to prepare the dish? (e.g., "1. Identify variables, 2. Write equations...")
*   **The Presentation:** How should the final dish look? (e.g., "Use `<think>` tags and `\boxed{}` for the answer")

System Prompts provide all this information to the LLM, ensuring it uses the *correct* reasoning style and produces the output in the *exact format* SoT expects.

## What's Inside a System Prompt?

Each SoT reasoning paradigm has its own unique System Prompt file. These aren't generated on the fly; they are carefully crafted text files stored within the SoT library.

Let's peek at the System Prompt for "Conceptual Chaining" in English. We can fetch it using the `get_system_prompt` method we saw briefly in Chapter 1:

```python
# Make sure SoT is initialized
from sketch_of_thought import SoT
sot = SoT()

# Get the prompt text for Conceptual Chaining in English
cc_prompt_text = sot.get_system_prompt(paradigm="conceptual_chaining", language_code="EN")

# Print the first few lines to get an idea
print('\n'.join(cc_prompt_text.split('\n')[:10])) # Show just the start
```

*Output (Beginning of the Conceptual Chaining prompt):*

```markdown
## **Role & Objective**  
You are a reasoning expert specializing in **structured concept linking** by connecting essential ideas in a logical sequence. Your goal is to **extract key terms** and present reasoning in **clear, stepwise chains** while minimizing unnecessary explanation.  

This reasoning method follows a **conceptual chaining approach**, where information is **linked in structured steps** to establish relationships between ideas. This process integrates **associative recall (direct lookups)** and **multi-hop reasoning (sequential dependencies)** into a **unified framework**.  

This method is most effective for:  
- **Commonsense reasoning** (quickly linking familiar ideas)  
- **Multi-hop inference** (tracing logical or causal dependencies)  
- **Fact-based recall** (retrieving knowledge with minimal cognitive load)  
```

This prompt immediately tells the LLM its "Role" (a concept linking expert) and "Objective" (extract key terms, use stepwise chains, be concise).

Let's break down the typical structure you'll find in these System Prompt files:

1.  **Role & Objective:**
    *   Sets the stage. Tells the LLM *what kind of expert* it should act like for this paradigm and *what its main goal* is.
    *   *Analogy:* The title and brief description on the recipe card (e.g., "Master Recipe: Quick & Easy Tomato Soup").

2.  **How to Apply / Step-by-Step Guide:**
    *   Provides concrete steps the LLM should follow to perform the reasoning.
    *   *Analogy:* The numbered instructions on the recipe card (e.g., "1. Chop onions. 2. Sauté garlic...").
    *   *Example (from Conceptual Chaining Prompt):*
        ```markdown
        1. **Extract Key Concepts** → Identify the most relevant words or entities.  
        2. **Use Minimal Words** → Keep each reasoning step **concise and direct**.  
        3. **Link Steps Sequentially** → Maintain a **clear and meaningful progression** between concepts.
        ... 
        ```

3.  **Rules & Directives:**
    *   Lists specific constraints, do's, and don'ts. These are crucial for ensuring the LLM adheres to the SoT style.
    *   *Analogy:* Important notes on the recipe card (e.g., "Do not over-stir," "Use low heat," "Serve immediately").
    *   *Example (from Conceptual Chaining Prompt):*
        ```markdown
        1. **Use Structured Concept Linking**
           - Each step **must be logically connected**.
           - Use arrows (`→`) to show dependencies.
        2. **Avoid Unnecessary Text**
           - **Do not** restate the question.
           - **Do not** use full sentences. 
        ...
        ```

4.  **Output Format:**
    *   Specifies *exactly* how the final reasoning and answer should be formatted, often using examples like the `<think>` and `\boxed{}` tags. This consistency is vital.
    *   *Analogy:* The "Plating Instructions" or a picture of the finished dish on the recipe card.
    *   *Example (from Conceptual Chaining Prompt):*
        ```markdown
        4. **Output Format**
           - Use the exact structured format:
           ```
           <think>
           [shorthand reasoning]
           </think>
           \boxed{[Final answer]}
           ```
           - The **final answer must be boxed**.
           - **Use minimal words in your response.** 
        ```

By providing these detailed instructions, System Prompts act as powerful guides, steering the LLM towards generating efficient, structured, and correctly formatted SoT-style reasoning.

## Why Separate Files?

SoT stores these prompts in separate `.md` (Markdown) files within its `config/prompts/` directory, organized by language (like `EN`, `KR`, `DE`, `IT`).

*   `config/prompts/EN/EN_ChunkedSymbolism_SystemPrompt.md`
*   `config/prompts/EN/EN_ConceptualChaining_SystemPrompt.md`
*   `config/prompts/KR/KR_ChunkedSymbolism_SystemPrompt.md`
*   ...and so on.

This approach has several advantages:

*   **Clarity:** The instructions for each paradigm are distinct and easy to read or modify.
*   **Maintainability:** If you want to tweak the instructions for a paradigm, you just edit the corresponding file.
*   **Extensibility:** Adding a new paradigm or language involves creating new prompt files.
*   **Multilingual Support:** Having separate files makes it easy to provide instructions in different languages, which we'll explore in the [next chapter](06_multilingual_support_.md).

## Under the Hood: How Prompts are Loaded and Used

You don't need to manually read these files. The [SoT Orchestrator](02_sot_orchestrator_.md) (`SoT` class) handles this automatically.

**Simple Walkthrough:**

1.  **Startup:** When you create the `SoT()` object, one of the first things it does is scan the `config/prompts/` directory. It finds all the language folders (like `EN`, `KR`) and reads the specific `.md` prompt files for each paradigm within those folders.
2.  **Caching:** It stores the text content of each prompt file in an internal dictionary (like a quick-reference binder) called `PROMPT_CACHE`. This cache is organized by language and paradigm name.
3.  **Retrieval:** When you call `sot.get_system_prompt(paradigm="...", language_code="...")`, the orchestrator simply looks up the requested prompt text in its `PROMPT_CACHE` and returns it instantly.

**Sequence Diagram:**

```mermaid
sequenceDiagram
    participant User
    participant Orchestrator as SoT()
    participant FileSystem as Prompt Files (.md)
    participant Cache as In-Memory PROMPT_CACHE

    User->>Orchestrator: Initialize SoT()
    Orchestrator->>FileSystem: Read all .md files in config/prompts/
    FileSystem-->>Orchestrator: Return prompt texts
    Orchestrator->>Cache: Store prompts by Language & Paradigm
    Note over Orchestrator, Cache: Startup Loading

    User->>Orchestrator: sot.get_system_prompt("conceptual_chaining", "EN")
    Orchestrator->>Cache: Fetch prompt for ['EN']['conceptual_chaining']
    Cache-->>Orchestrator: Return stored prompt text
    Orchestrator-->>User: Provide prompt text
end
```

**Code Glimpse:**

Let's see how this looks in simplified code within `sketch_of_thought/sketch_of_thought.py`:

*   **Initialization (`__init__`)**: Sets up paths and triggers loading.
    ```python
    # Inside the SoT class __init__ method (simplified)
    import os
    from .config.config import default_path

    class SoT:
        def __init__(self):
            # ... (load model, tokenizer, etc.) ...
            
            # Define base path for prompt files
            self.__PROMPT_PATH_BASE = os.path.join(str(default_path()), "config/prompts/")
            
            # Map internal paradigm names to their prompt filenames
            self.__PROMPT_FILENAMES = {
                "chunked_symbolism": "ChunkedSymbolism_SystemPrompt.md",
                "expert_lexicons": "ExpertLexicons_SystemPrompt.md",
                "conceptual_chaining": "ConceptualChaining_SystemPrompt.md",
            }

            # Create an empty cache to store prompts later
            self.PROMPT_CACHE = {}
            
            # Preload contexts first (to know available languages)
            self.__preload_contexts() # Reads exemplars.json
            self.__LANGUAGE_CODES = list(self.CONTEXT_CACHE.keys()) # Finds 'EN', 'KR', etc.

            # NOW, load all prompts into the cache
            self.__preload_prompts() 
            
            # ... (rest of init) ...
    ```
    This part identifies where the prompt files are and which filename corresponds to which paradigm. It then calls `__preload_prompts`.

*   **Preloading Prompts (`__preload_prompts`)**: Reads files into the cache.
    ```python
    # Inside the SoT class (simplified)
        def __preload_prompts(self):
            """Loads all available system prompts into memory."""
            # Loop through detected languages (e.g., 'EN', 'KR')
            for lang in self.__LANGUAGE_CODES:
                self.PROMPT_CACHE[lang] = {} # Create sub-dictionary for this language
                # Loop through known paradigms (e.g., 'chunked_symbolism')
                for paradigm, filename in self.__PROMPT_FILENAMES.items():
                    # Construct the full path to the specific prompt file
                    file_path = os.path.join(self.__PROMPT_PATH_BASE, lang, f"{lang}_{filename}")
                    # Check if the file exists
                    if os.path.exists(file_path):
                        # Read the file content
                        with open(file_path, "r", encoding="utf-8") as file:
                            # Store the content in the cache
                            self.PROMPT_CACHE[lang][paradigm] = file.read()
    ```
    This helper method, called during initialization, does the actual reading of `.md` files and fills the `PROMPT_CACHE` dictionary.

*   **Getting a Prompt (`get_system_prompt`)**: Retrieves from the cache.
    ```python
    # Inside the SoT class (simplified)
    import copy # Used to return a copy, not the original

    class SoT:
        # ... (init, __preload_prompts, etc.) ...

        def get_system_prompt(self, paradigm="chunked_symbolism", language_code="EN"):
            """Retrieves the preloaded system prompt from the cache."""
            
            # Basic checks (omitted for brevity) ensuring paradigm & language are valid...
            # assert paradigm in self.avaliable_paradigms(), ...
            # assert language_code in self.avalilable_languages(), ...
            
            # Directly access the cache using language and paradigm keys
            prompt_text = self.PROMPT_CACHE[language_code][paradigm]
            
            # Return a copy of the stored text
            return copy.deepcopy(prompt_text)
    ```
    This method simply performs a quick lookup in the `PROMPT_CACHE` dictionary, making access very fast after the initial loading.

## Conclusion

In this chapter, we explored **System Prompts**, the detailed "recipe cards" that guide the LLM on *how* to use each SoT [Reasoning Paradigm](01_reasoning_paradigms_.md). We learned:

*   They define the **goal, steps, rules, and output format** for each paradigm.
*   They are stored as separate **`.md` files** for clarity and easy modification.
*   You can view them using `sot.get_system_prompt()`.
*   SoT **pre-loads** these prompts into a cache during initialization for fast access.
*   They are a crucial part of the context prepared by `get_initialized_context`, ensuring the LLM behaves correctly and efficiently.

These prompts, stored as separate files for different languages, are key to SoT's ability to work across multiple languages. How does that work? Let's find out in the next chapter: [Multilingual Support](06_multilingual_support_.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)