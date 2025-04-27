# Chapter 6: Multilingual Support

In the [previous chapter](05_system_prompts_.md), we looked closely at **System Prompts** – the detailed instruction guides that tell the Language Model exactly how to use each SoT [Reasoning Paradigm](01_reasoning_paradigms_.md). We saw that these prompts are stored in separate files, which leads us nicely into our final topic: how SoT handles different languages.

Imagine using your favorite app, like a map or a game. Often, you can go into the settings and change the language of the menus and instructions, right? The app's core function (showing maps or playing the game) stays the same, but the way it communicates with you changes to your preferred language.

**Multilingual Support** in SoT works just like that!

## Speaking the User's Language

SoT is designed to be used by people and with AI models that might operate in different languages. If you ask a question in Korean, it's much more effective if the thinking instructions (System Prompt) and the examples (Exemplars) given to the LLM are *also* in Korean. This ensures the guidance matches the language of the task.

SoT makes this easy by providing its core prompts and examples in multiple languages (currently English `EN`, Korean `KR`, Italian `IT`, and German `DE`). The underlying reasoning logic (like how Chunked Symbolism works) doesn't change, but the *description* of that logic adapts to the selected language.

**Use Case:** Let's say you want to ask a math question in Korean and want SoT to prepare the context (instructions and examples) for an LLM in Korean.

## How It Works: Language Codes

SoT identifies languages using standard two-letter codes:

*   `EN`: English
*   `KR`: Korean
*   `IT`: Italian
*   `DE`: German

When you want SoT to operate in a specific language, you simply tell it which language code to use.

## Using Different Languages in SoT

You control the language using the `language_code` parameter in the key methods we've already learned about.

**1. Listing Available Languages**

First, you can easily check which languages your SoT installation supports:

```python
# Make sure SoT is initialized
from sketch_of_thought import SoT
sot = SoT()

# Get the list of supported language codes
supported_languages = sot.avalilable_languages()
print(f"Supported languages: {supported_languages}") 
```

*Output:*

```
Supported languages: ['EN', 'DE', 'IT', 'KR'] # Order might vary
```

This tells us that this version of SoT comes with resources for English, German, Italian, and Korean.

**2. Getting a System Prompt in a Specific Language**

Let's get the System Prompt for "Chunked Symbolism", but this time, we'll ask for the Korean version:

```python
# Get the Korean system prompt for Chunked Symbolism
korean_cs_prompt = sot.get_system_prompt(
    paradigm="chunked_symbolism", 
    language_code="KR" # Specify Korean!
)

# Print the first few lines (Output will be in Korean)
print('\n'.join(korean_cs_prompt.split('\n')[:5])) 
```

*Output (Beginning of the Korean prompt):*

```markdown
## **역할 및 목표**
당신은 **Chunked Symbolism**이라 불리는 인지적 추론 기법을 전문으로 하는 추론 전문가입니다. 이 기법은 수치적 추론을 구조화된 단계로 조직합니다. 당신의 목표는 **최소한의 단어**를 사용하면서, 정보를 **방정식, 변수, 단계별 산술**로 표현하여 **Chunked Symbolism**을 활용하는 것입니다.

Chunked Symbolism은 **청킹(chunking)**이라는 인지 과학 원리에 영감을 받았습니다. 이는 관련 정보를 의미 있는 단위로 묶었을 때, 사람이 정보를 더 효율적으로 처리한다는 아이디어입니다. 문제를 자유형식으로 푸는 대신, **Chunked Symbolism은 복잡한 연산을 더 작고 구조화된 단계로 나눕니다**.

```

It's the same "Chunked Symbolism" recipe card as we saw in English, but translated into Korean!

**3. Getting Formatted Context in a Specific Language**

Now, let's prepare the full context package (System Prompt + Examples + User Question) for our Korean math question.

```python
# Our question (in Korean)
korean_question = "앨리스는 사과 5개를 가지고 있습니다. 그녀는 밥에게 사과 3개를 줍니다. 앨리스는 몇 개의 사과를 가지고 있습니까?"
paradigm = "chunked_symbolism" # Assumed from classify_question

# Get the context formatted for an LLM, using Korean resources
korean_context = sot.get_initialized_context(
    paradigm=paradigm,
    question=korean_question,
    language_code="KR",      # Specify Korean!
    include_system_prompt=True,
    format="llm"
)

# Print the first item (System Prompt) and the last item (User Question)
print("First item (System Prompt in Korean):")
print(korean_context[0]['content'][:100] + "...") # Show beginning of Korean system prompt

print("\nLast item (User Question in Korean):")
print(korean_context[-1])
```

*Output:*

```
First item (System Prompt in Korean):
## **역할 및 목표**
당신은 **Chunked Symbolism**이라 불리는 인지적 추론 기법을 전문으로 하는 추론 전문가입니다. 이 기법은 수치적 추론을 구조화된 단계로 조직합니다. 당신의 목표는 **최소한의 단어**를 ...

Last item (User Question in Korean):
{'role': 'user', 'content': '앨리스는 사과 5개를 가지고 있습니다. 그녀는 밥에게 사과 3개를 줍니다. 앨리스는 몇 개의 사과를 가지고 있습니까?'}
```

As you can see, `get_initialized_context` used the `language_code="KR"` instruction to fetch the Korean system prompt and Korean examples (which are inside the `korean_context` list between the first and last items, though we didn't print them here). It then appended our Korean question at the end. This package is now ready to be sent to an LLM that understands Korean, guiding it with instructions and examples in the same language.

## Under the Hood: How Language Resources are Organized

SoT manages multilingual resources through simple file organization and data structures:

1.  **System Prompts:** As mentioned in the [previous chapter](05_system_prompts_.md), prompts are stored in `.md` files. They are organized into subdirectories named after the language code within `sketch_of_thought/config/prompts/`.
    *   `config/prompts/EN/EN_ChunkedSymbolism_SystemPrompt.md`
    *   `config/prompts/KR/KR_ChunkedSymbolism_SystemPrompt.md`
    *   `config/prompts/IT/IT_ChunkedSymbolism_SystemPrompt.md`
    *   `config/prompts/DE/DE_ChunkedSymbolism_SystemPrompt.md`
    *   ... and similarly for `ConceptualChaining` and `ExpertLexicons`.

2.  **Exemplars (Examples):** The example question-answer pairs are stored in a single JSON file: `sketch_of_thought/config/exemplars.json`. Inside this file, the examples are organized by language code as the top-level keys, and then by paradigm name.
    ```json
    // Simplified structure of exemplars.json
    {
      "EN": {
        "chunked_symbolism": [
          {"question": "English Q1...", "answer": "English A1..."}
          // ... more English CS examples
        ],
        "conceptual_chaining": [
          // ... English CC examples
        ]
        // ... more English paradigms
      },
      "KR": {
        "chunked_symbolism": [
          {"question": "Korean Q1...", "answer": "Korean A1..."}
          // ... more Korean CS examples
        ],
        "conceptual_chaining": [
          // ... Korean CC examples
        ]
        // ... more Korean paradigms
      },
      // ... entries for IT, DE, etc.
    }
    ```

**Loading and Caching:**

When you initialize the [SoT Orchestrator](02_sot_orchestrator_.md) (`sot = SoT()`), it automatically:

1.  **Reads `exemplars.json`:** It loads the entire JSON file into the `CONTEXT_CACHE` dictionary in memory. The language codes (`"EN"`, `"KR"`, etc.) become the keys in this cache. It uses these keys to determine the available languages (`self.__LANGUAGE_CODES`).
2.  **Scans Prompt Directories:** It looks inside `config/prompts/` for folders matching the language codes found in step 1 (e.g., `EN`, `KR`).
3.  **Reads Prompt Files:** For each language and each known paradigm, it reads the corresponding `.md` file (e.g., `config/prompts/KR/KR_ChunkedSymbolism_SystemPrompt.md`).
4.  **Populates `PROMPT_CACHE`:** It stores the content of each prompt file in the `PROMPT_CACHE` dictionary, again organized by language code and then paradigm name.

**Retrieval:**

When you call `get_system_prompt(paradigm="...", language_code="KR")` or `get_initialized_context(..., language_code="KR")`:

1.  The method receives the `language_code` (e.g., `"KR"`).
2.  It uses this code as the first key to look up the relevant data in the pre-loaded `PROMPT_CACHE` or `CONTEXT_CACHE`.
3.  It then uses the `paradigm` name as the second key to get the specific prompt text or list of examples for that language and paradigm.

This design makes adding new languages straightforward (add a new language folder under `prompts/`, add a new top-level key to `exemplars.json`, and translate the content) and keeps language selection fast during runtime because everything is loaded into memory upfront.

**Sequence Diagram:**

```mermaid
sequenceDiagram
    participant User
    participant Orchestrator as SoT()
    participant FileSystem as Prompt/Exemplar Files
    participant Cache as In-Memory Caches

    User->>Orchestrator: Initialize SoT()
    Orchestrator->>FileSystem: Read exemplars.json
    FileSystem-->>Orchestrator: Return JSON data
    Orchestrator->>Cache: Store contexts by Lang/Paradigm (CONTEXT_CACHE)
    Note right of Orchestrator: Detect languages (EN, KR...)
    Orchestrator->>FileSystem: Read .md files from config/prompts/EN, config/prompts/KR...
    FileSystem-->>Orchestrator: Return prompt texts
    Orchestrator->>Cache: Store prompts by Lang/Paradigm (PROMPT_CACHE)
    Note over Orchestrator, Cache: Startup Loading

    User->>Orchestrator: get_initialized_context(..., language_code="KR")
    Orchestrator->>Cache: Fetch prompt for ['KR'][paradigm] (from PROMPT_CACHE)
    Cache-->>Orchestrator: Return Korean prompt text
    Orchestrator->>Cache: Fetch exemplars for ['KR'][paradigm] (from CONTEXT_CACHE)
    Cache-->>Orchestrator: Return Korean examples list
    Note right of Orchestrator: Assemble context using Korean resources
    Orchestrator-->>User: Provide context with Korean prompt/examples
end
```

**Code Glimpse:**

Let's revisit simplified snippets showing how the language code is used:

*   **Loading Contexts (`__preload_contexts`)**: Reads `exemplars.json` and stores it, inherently capturing the language keys.
    ```python
    # Inside the SoT class (simplified)
    import json
    import os
    from .config.config import default_path

    class SoT:
        def __init__(self):
            # ... paths ...
            self.__CONTEXT_PATH_BASE = os.path.join(str(default_path()), "config/exemplars.json")
            self.CONTEXT_CACHE = {}
            # ... other caches ...

            self.__preload_contexts() # Load the JSON
            # Determine available languages DIRECTLY from the loaded JSON keys
            self.__LANGUAGE_CODES = list(self.CONTEXT_CACHE.keys()) 
            
            self.__preload_prompts() # Now load prompts based on detected languages
            # ... rest of init ...

        def __preload_contexts(self):
            """Loads all available contexts (exemplars) into memory."""
            with open(self.__CONTEXT_PATH_BASE, "r", encoding="utf-8") as f:
                self.CONTEXT_CACHE = json.load(f) # Loads EN, KR, IT, DE keys etc.
    ```
    This shows how the available languages are determined by the top-level keys in `exemplars.json`.

*   **Loading Prompts (`__preload_prompts`)**: Uses the detected languages to find the right folders.
    ```python
    # Inside the SoT class (simplified)
        def __preload_prompts(self):
            """Loads system prompts for all detected languages."""
            # self.__LANGUAGE_CODES was set in __init__ after __preload_contexts
            for lang in self.__LANGUAGE_CODES: # Iterate through 'EN', 'KR', etc.
                self.PROMPT_CACHE[lang] = {} # Initialize cache for this language
                for paradigm, filename in self.__PROMPT_FILENAMES.items():
                    # Construct path like config/prompts/KR/KR_ChunkedSymbolism_SystemPrompt.md
                    file_path = os.path.join(self.__PROMPT_PATH_BASE, lang, f"{lang}_{filename}")
                    if os.path.exists(file_path):
                        with open(file_path, "r", encoding="utf-8") as file:
                            # Store under the language key: self.PROMPT_CACHE['KR'][paradigm]
                            self.PROMPT_CACHE[lang][paradigm] = file.read() 
    ```
    This method explicitly uses the `lang` variable (e.g., "KR") to build the file path and organize the cache.

*   **Getting Context (`get_initialized_context`)**: Uses `language_code` to access the correct cache entries.
    ```python
    # Inside the SoT class (simplified)
    import copy

    class SoT:
        # ... (init, loading methods) ...

        def get_initialized_context(self, paradigm, question=None, image_data=None, 
                                    language_code="EN", # <-- The parameter we use
                                    include_system_prompt=True, format="llm"):
            
            # Assert language_code is valid (uses self.avalilable_languages())
            assert language_code in self.avalilable_languages(), f"`{language_code}` is not compatible!"
            
            if format.lower() == "llm":
                # Fetch examples for the SPECIFIED language and paradigm
                exemplars = self.CONTEXT_CACHE[language_code][paradigm] # <-- Uses language_code
                
                context = []
                if include_system_prompt:
                    # Get prompt for the SPECIFIED language (calls get_system_prompt)
                    prompt_text = self.get_system_prompt(paradigm=paradigm, language_code=language_code) # <-- Passes language_code
                    context.append({"role": "system", "content": prompt_text})

                # Add examples (already fetched for the correct language)
                for ex in exemplars:
                     context.append({"role": "user", "content": ex['question']})
                     context.append({"role": "assistant", "content": ex['answer']})

                # ... add user question ...
                return context

            # ... (VLM and Raw formats also use language_code to access CONTEXT_CACHE) ...
            elif format.lower() == "raw":
                 return copy.deepcopy(self.CONTEXT_CACHE[language_code][paradigm]) # <-- Uses language_code

        def get_system_prompt(self, paradigm="chunked_symbolism", language_code="EN"): # <-- The parameter
             # Assert language_code is valid...
             # Retrieve from cache using BOTH language and paradigm
             prompt_text = self.PROMPT_CACHE[language_code][paradigm] # <-- Uses language_code
             return copy.deepcopy(prompt_text)
    ```
    These snippets clearly show how the `language_code` parameter flows through the methods to select the correct resources from the caches.

## Conclusion

In this chapter, we learned about **Multilingual Support** in SoT. Key takeaways include:

*   SoT provides System Prompts and Exemplars in multiple languages (EN, KR, IT, DE shown).
*   You control the language using the `language_code` parameter in methods like `get_system_prompt` and `get_initialized_context`.
*   The core reasoning logic remains the same, but the instructions and examples adapt to the chosen language.
*   Resources are organized by language code in the configuration files and loaded into caches for efficient access.
*   You can check supported languages with `sot.avalilable_languages()`.

This feature makes SoT more accessible and effective for users and AI models working in different linguistic contexts.

This concludes our introductory tour through the core concepts of the Sketch-of-Thought framework! We've covered the different [Reasoning Paradigms](01_reasoning_paradigms_.md), how the [SoT Orchestrator](02_sot_orchestrator_.md) manages the process, the role of the [Paradigm Selection Model](03_paradigm_selection_model_.md), how [Context Initialization & Formatting](04_context_initialization___formatting_.md) prepares the input for the LLM, the details of [System Prompts](05_system_prompts_.md), and finally, how SoT supports [Multilingual Support](06_multilingual_support_.md). We hope this gives you a solid foundation for using and understanding SoT!

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)