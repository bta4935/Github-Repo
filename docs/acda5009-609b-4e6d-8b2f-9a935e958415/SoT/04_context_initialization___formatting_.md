# Chapter 4: Context Initialization & Formatting

In the [previous chapter](03_paradigm_selection_model_.md), we saw how the SoT Orchestrator uses its clever helper, the [Paradigm Selection Model](03_paradigm_selection_model_.md), to automatically figure out the *best* reasoning style (like `chunked_symbolism` or `conceptual_chaining`) for your question. That's like the receptionist directing you to the right department.

But once you're at the right department, how do you present your problem clearly so they can solve it efficiently? You need to give them the right background information, show them examples of what you expect, and then state your specific problem.

This process of preparing the *complete package* of information for the final AI brain (the Large Language Model or LLM) is called **Context Initialization & Formatting**. This chapter explains how SoT handles this crucial setup step.

## Setting the Stage for the LLM

Imagine you're setting up a classroom for a very specific lesson. You wouldn't just write the day's problem on the board and expect students to know how to solve it in the exact way you want. Instead, you would:

1.  **Put up Posters:** These posters explain the *rules* and *methods* for this specific lesson (this is like the **System Prompt**).
2.  **Show Examples:** You'd write a few solved examples on the board, showing the *exact steps* and *format* required (these are the **Exemplars** or few-shot examples).
3.  **Present the Problem:** Finally, you'd write the actual problem the students need to solve today (this is the **User's Question**).

**Context Initialization & Formatting** in SoT is exactly like this classroom setup. It takes these three pieces – the rules (System Prompt), the examples (Exemplars), and the specific problem (User Question) – and arranges them perfectly into a single package that the LLM can understand and use effectively.

Why is this important? LLMs work best when they have clear instructions and examples that match the task. SoT prepares this context to guide the LLM to use the chosen reasoning paradigm correctly and efficiently.

## Assembling the Context with `get_initialized_context`

The main tool SoT provides for this is the `get_initialized_context` method, which belongs to the [SoT Orchestrator](02_sot_orchestrator_.md) (the `SoT` class).

Let's say we used `classify_question` and found that the best paradigm for "Alice has 5 apples and gives 3 to Bob. How many does she have left?" is `chunked_symbolism`. Now, we use `get_initialized_context` to build the final input package:

```python
# Make sure you have initialized SoT first
from sketch_of_thought import SoT
sot = SoT() 

# Our question and the chosen paradigm
question = "Alice has 5 apples and gives 3 to Bob. How many does she have left?"
paradigm = "chunked_symbolism" # We determined this earlier
language = "EN" # We want English instructions

# Use the method to assemble the context
formatted_context = sot.get_initialized_context(
    paradigm=paradigm,          # Which reasoning style to use
    question=question,          # Our specific question
    language_code=language,     # Language for prompts/examples
    include_system_prompt=True, # Yes, include the "rules" poster
    format="llm"                # Format for a standard text LLM
)

# Let's peek at the structure (it's a list) and the last item
print(f"Number of items in context: {len(formatted_context)}")
print("Last item (our question):")
print(formatted_context[-1]) 
```

*Output:*

```
Number of items in context: 6 
Last item (our question):
{'role': 'user', 'content': 'Alice has 5 apples and gives 3 to Bob. How many does she have left?'}
```

What happened here? `get_initialized_context` did the following:

1.  Fetched the **System Prompt** for `chunked_symbolism` in English.
2.  Fetched the pre-written **Exemplars** (example Q&A pairs) for `chunked_symbolism` in English.
3.  Added our specific **User Question**.
4.  Formatted all of this into a list, ready for an LLM. The output `formatted_context` now contains the system prompt, the example interactions, and finally our question, all structured correctly.

## Understanding the Different Formats: `llm`, `vlm`, `raw`

You might have noticed the `format="llm"` parameter. SoT can prepare the context in a few different ways, depending on what kind of AI model you're sending it to.

1.  **`format="llm"` (Default):**
    *   **What it is:** This is the standard format for most text-based Large Language Models (like GPT, Llama, Mistral, Qwen).
    *   **Structure:** It creates a list of dictionaries. Each dictionary has a `role` (`system`, `user`, or `assistant`) and `content` (the actual text). This mimics a conversation history.
    *   **Example Structure:**
        ```python
        [
          {'role': 'system', 'content': 'System prompt text...'},
          {'role': 'user', 'content': 'Example Question 1...'},
          {'role': 'assistant', 'content': 'Example Answer 1...'},
          # ... more examples ...
          {'role': 'user', 'content': 'Your actual question...'}
        ]
        ```
    *   **When to use:** Use this for almost any text-only chatbot or language model interaction.

2.  **`format="vlm"`:**
    *   **What it is:** This format is for **V**ision-**L**anguage **M**odels – AI models that can understand *both* text and images.
    *   **Structure:** It's similar to `llm`, but the `content` is slightly different. It's a list containing dictionaries that specify the `type` (`text` or `image`) and the actual data.
    *   **Example Structure (for the user's turn with an image):**
        ```python
        # ... previous messages ...
        {
          'role': 'user', 
          'content': [
            {'type': 'text', 'text': 'Your question about the image...'},
            {'type': 'image', 'image': image_data} # Image data goes here
          ]
        }
        ```
    *   **When to use:** Use this *only* if you are working with a multimodal model and need to include image data along with your text question (passed via the `image_data` parameter in `get_initialized_context`). If you use `vlm` without image data, it will still work but might issue a warning. If you provide image data but use `format="llm"`, the image will be ignored.

3.  **`format="raw"`:**
    *   **What it is:** This option doesn't format anything for an LLM. It just gives you the raw list of example questions and answers (Exemplars) for the chosen paradigm and language. The System Prompt is *not* included in this format.
    *   **Structure:** A simple list of dictionaries, each containing a `question` and its corresponding `answer`.
        ```python
        [
          {'question': 'Example Question 1...', 'answer': 'Example Answer 1...'},
          {'question': 'Example Question 2...', 'answer': 'Example Answer 2...'},
          # ... more examples ...
        ]
        ```
    *   **When to use:** Use this if you want to create your own custom formatting or just inspect the example data SoT uses.

```python
# Get the raw examples for Conceptual Chaining
raw_examples = sot.get_initialized_context(
    paradigm="conceptual_chaining",
    language_code="EN",
    format="raw" 
    # Note: question and include_system_prompt are ignored for raw format
)

# Print the first raw example
print("First raw example:")
print(raw_examples[0])
```

*Output:*

```
First raw example:
{'question': "Is it possible for a planet to be entirely covered in ocean?", 'answer': '<think>\nPlanet -> Covered entirely -> Ocean -> Possible?\nOcean world concept -> Exists in astronomy/astrobiology -> Theoretical support\nRequires conditions -> Sufficient water volume -> Stable temperature range (liquid water) -> Atmospheric pressure\nKnown examples? -> None confirmed, but candidates exist (e.g., exoplanets like GJ 1214 b suggested)\nConclusion: Theoretically possible, conditions demanding, no confirmed examples yet.\n</think>\n\nYes, it is theoretically possible for a planet to be entirely covered in ocean, often referred to as an "ocean world" or "water world". Such planets would require specific conditions like sufficient water volume and a stable temperature range to maintain liquid water across the entire surface. While no confirmed examples exist in our solar system, several exoplanets are considered potential candidates.'}
```

This gives you just the question/answer pairs stored within SoT for that paradigm.

## Under the Hood: Assembling the Package

How does `get_initialized_context` actually build these different formats? It's quite straightforward:

1.  **Check Inputs:** It first makes sure the requested `paradigm` and `language_code` are valid.
2.  **Fetch Data:** Based on the `paradigm` and `language_code`, it retrieves the correct pre-loaded data from its internal storage:
    *   The [System Prompts](05_system_prompts_.md) (from `PROMPT_CACHE`).
    *   The list of Exemplars (from `CONTEXT_CACHE`).
3.  **Format Output:** It then checks the requested `format`:
    *   If `"llm"`: It creates a list. If `include_system_prompt` is `True`, it adds the system prompt as the first item (`{'role': 'system', ...}`). Then, it loops through the fetched exemplars, adding each question (`{'role': 'user', ...}`) and answer (`{'role': 'assistant', ...}`). Finally, if a `question` was provided, it adds that at the end (`{'role': 'user', ...}`).
    *   If `"vlm"`: It does the same assembly as `"llm"`, but wraps the text content inside `[{'type': 'text', 'text': ...}]`. If `image_data` is provided with the user `question`, it adds that image element to the final user message. It also issues warnings if image data is missing or if `llm` format was used with image data.
    *   If `"raw"`: It simply returns a copy of the fetched list of exemplars directly.
4.  **Return:** It returns the assembled list (or the raw list).

Here's a simplified view of the process for the `llm` format:

```mermaid
sequenceDiagram
    participant User
    participant Orchestrator as SoT()
    participant Cache as In-Memory Storage

    User->>Orchestrator: get_initialized_context(paradigm="chunked_symbolism", question="Alice apples...", format="llm", include_system_prompt=True)
    Orchestrator->>Cache: Get 'chunked_symbolism' prompt (EN)
    Cache-->>Orchestrator: Return prompt text
    Orchestrator->>Cache: Get 'chunked_symbolism' exemplars (EN)
    Cache-->>Orchestrator: Return list of Q&A examples
    Note right of Orchestrator: Start building the output list:\n1. Add system prompt {'role':'system',...}\n2. Add examples {'role':'user',...}, {'role':'assistant',...}\n3. Add user question {'role':'user',...}
    Orchestrator-->>User: Return the final formatted list
end
```

**Code Glimpse:**

Let's look at a *simplified* version of the `get_initialized_context` method inside `sketch_of_thought/sketch_of_thought.py` focusing on the `llm` format logic:

```python
# Inside the SoT class (simplified for clarity)
import copy 
from loguru import logger # Used for warnings
from .config.warnings import MULTIMODAL_MISALIGNMENT, NO_IMAGE # Warning messages

class SoT:
    # ... (other methods like __init__, classify_question) ...

    def get_initialized_context(self, paradigm, question=None, image_data=None, 
                                language_code="EN", include_system_prompt=True, 
                                format="llm"):
        
        # Basic checks (ensure paradigm and language are valid - omitted here) ...

        # --- Handle LLM format ---
        if format.lower() == "llm":
            # Warn if user provided an image but chose 'llm' format
            if image_data:
                logger.warning(MULTIMODAL_MISALIGNMENT) 
            
            # Get the examples for this paradigm/language from cache
            exemplars = self.CONTEXT_CACHE[language_code][paradigm]
            
            # Start building the context list
            context = []
            if include_system_prompt:
                # Get the system prompt from cache and add it first
                system_prompt_text = self.get_system_prompt(paradigm=paradigm, language_code=language_code)
                context.append({"role": "system", "content": system_prompt_text})

            # Add the examples (Exemplars) from the cache
            for ex in exemplars:
                context.append({"role": "user", "content": ex['question']})
                context.append({"role": "assistant", "content": ex['answer']})
            
            # Add the user's actual question if provided
            if question and question != "":
                context.append({"role": "user", "content": question})

            return context # Return the fully formatted list

        # --- Handle VLM format ---
        elif format.lower() == "vlm":
            # (Similar logic, but wraps content in [{'type':'text', ...}])
            # (Handles adding image_data if present)
            # (Issues NO_IMAGE warning if needed)
            # ... implementation omitted for brevity ...
            pass # Placeholder for VLM logic

        # --- Handle Raw format ---
        else: # format == "raw"
            # Just return a copy of the examples from the cache
            return copy.deepcopy(self.CONTEXT_CACHE[language_code][paradigm])

```

This snippet shows how the method accesses the pre-loaded `CONTEXT_CACHE` (holding exemplars) and `PROMPT_CACHE` (via `get_system_prompt`) and then constructs the list of dictionaries according to the standard `llm` chat format. The logic for `vlm` and `raw` follows similar principles but adjusts the final structure.

## Conclusion

In this chapter, we learned about **Context Initialization & Formatting** – the crucial step where SoT assembles all the necessary information into a package ready for the LLM. We saw:

*   It combines the **System Prompt** (the rules), **Exemplars** (the examples), and the **User Question** (the problem).
*   The main tool is the `get_initialized_context` method of the `SoT` class.
*   It supports different output **formats** (`llm` for text models, `vlm` for vision-language models, `raw` for unprocessed examples) to suit various needs.
*   This process ensures the LLM receives clear instructions and relevant examples tailored to the chosen reasoning paradigm, guiding it towards an efficient and accurate SoT-style response.

We've now seen how SoT chooses a paradigm and prepares the input. One key piece of this input is the System Prompt – those "instructional posters" we talked about. What exactly do these prompts contain, and how are they designed?

Let's dive deeper into the instructions themselves in the next chapter: [System Prompts](05_system_prompts_.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)