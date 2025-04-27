# Chapter 1: Reasoning Paradigms

Welcome to the Sketch-of-Thought (SoT) tutorial! We're excited to guide you through this efficient framework for language model reasoning.

Imagine you have a question for an AI assistant. Sometimes you might ask a simple factual question ("What's the capital of France?"), sometimes a math problem ("If I have 5 apples and eat 2, how many are left?"), and sometimes something technical ("Explain Ohm's law using standard symbols").

How can an AI figure out the *best* way to think through each of these *different* types of questions efficiently, without writing a long essay each time? This is where **Reasoning Paradigms** come in!

## What Are Reasoning Paradigms?

Think of Reasoning Paradigms as specialized tools in a toolbox. Just like you wouldn't use a hammer to tighten a screw, you wouldn't use the same thinking style for every type of problem. SoT defines specific "thinking styles" or strategies, called paradigms, each designed for a particular kind of task.

The goal is to produce *concise* reasoning steps – just the essential sketch of the thought process – saving time and computational resources compared to more verbose methods.

SoT uses three core Reasoning Paradigms:

1.  **Conceptual Chaining:**
    *   **What it is:** This paradigm connects key ideas or concepts in a logical sequence, like forming a chain. It focuses on the relationships between important words or facts.
    *   **When it's used:** Great for commonsense questions, problems requiring multiple logical steps (multi-hop inference), or recalling facts.
    *   **Analogy:** Think of using **pliers** to grip and link different pieces together in the right order.
    *   **Simple Example:**
        *   *Question:* "If I leave ice cream in the sun, what happens?"
        *   *Conceptual Chaining thought:* `Ice cream → Sun (heat) → Melts`

2.  **Chunked Symbolism:**
    *   **What it is:** This paradigm breaks down problems involving numbers or symbols into structured steps, using variables and equations.
    *   **When it's used:** Perfect for math problems (arithmetic, algebra), symbolic logic, or technical calculations.
    *   **Analogy:** Like using a **wrench** that fits specific bolts (numbers and mathematical operations).
    *   **Simple Example:**
        *   *Question:* "Alice has 5 apples and gives 3 to Bob. How many does she have left?"
        *   *Chunked Symbolism thought:*
            ```
            A = 5 (Alice's apples)
            G = 3 (Given away)
            Remaining = A - G
            Remaining = 5 - 3
            Remaining = 2
            ```

3.  **Expert Lexicons:**
    *   **What it is:** This paradigm uses specialized shorthand, technical terms, symbols, and jargon specific to a particular field (like science, medicine, or programming). It packs a lot of information into very few characters.
    *   **When it's used:** Ideal for technical domains where experts use precise, condensed language.
    *   **Analogy:** Similar to using a **multimeter** in electronics – a specialized tool using symbols and readings understood by experts.
    *   **Simple Example:**
        *   *Question:* "What's the relationship between Voltage, Current, and Resistance?"
        *   *Expert Lexicons thought:* `V = I * R (Ohm's Law)`

The beauty of SoT is that it doesn't just *have* these tools; it aims to automatically pick the *right* tool for the job using its [Paradigm Selection Model](03_paradigm_selection_model_.md). We'll explore that automatic selection later, but first, let's see how we can interact with these paradigms directly.

## Working with Paradigms in Code

You can easily see which paradigms are available and explore their underlying instructions (called "System Prompts").

Let's initialize SoT first:

```python
# Import the SoT class
from sketch_of_thought import SoT

# Create an SoT object
sot = SoT()
```

This simple setup loads the necessary components, including the paradigm definitions.

Now, let's list the available paradigms:

```python
# Get the list of available paradigms
paradigms = sot.avaliable_paradigms()
print(paradigms)
```

*Output:*

```
['chunked_symbolism', 'conceptual_chaining', 'expert_lexicons']
```

This confirms the three core paradigms we discussed.

Each paradigm has a specific set of instructions (a "System Prompt") that tells the language model *how* to think using that style. You can retrieve these prompts:

```python
# Get the system prompt for Conceptual Chaining in English
cc_prompt = sot.get_system_prompt(paradigm="conceptual_chaining", language_code="EN")

# Print the first few lines (it's quite detailed!)
print('\n'.join(cc_prompt.split('\n')[:5])) # Show just the start
```

*Output (beginning of the prompt):*

```
## **Role & Objective**  
You are a reasoning expert specializing in **structured concept linking** by connecting essential ideas in a logical sequence. Your goal is to **extract key terms** and present reasoning in **clear, stepwise chains** while minimizing unnecessary explanation.  

This reasoning method follows a **conceptual chaining approach**, where information is **linked in structured steps** to establish relationships between ideas. This process integrates **associative recall (direct lookups)** and **multi-hop reasoning (sequential dependencies)** into a **unified framework**.  
```

This prompt guides the AI to use the "Conceptual Chaining" method. Similarly, `chunked_symbolism` and `expert_lexicons` have their own specific instructions.

SoT also comes with example question-answer pairs (exemplars) for each paradigm to show the AI exactly what the output should look like. You can fetch these too:

```python
# Get raw example data for Chunked Symbolism in English
cs_examples = sot.get_initialized_context(
    paradigm="chunked_symbolism", 
    language_code="EN",
    format="raw" # Get the raw list of examples
)

# Print the first example
print(cs_examples[0])
```

*Output (one example):*

```python
{'question': 'How much is $100 plus 15%? Format the final answer as a dollar amount.', 'answer': '<think>\nInitial Amount = $100\nPercentage = 15% = 0.15\nIncrease = Initial Amount * Percentage\nIncrease = $100 * 0.15\nIncrease = $15\nFinal Amount = Initial Amount + Increase\nFinal Amount = $100 + $15\nFinal Amount = $115\n</think>\n\\boxed{$115}'}
```

This shows a math problem (`question`) and its solution (`answer`) formatted precisely according to the Chunked Symbolism rules (using `<think>` tags and a `\boxed{}` final answer).

## Under the Hood: How Paradigms are Managed

SoT keeps things organized internally. It doesn't generate these rules or examples on the fly. Instead, it loads them when it starts up.

**Simple Walkthrough:**

1.  **Startup:** When you create the `SoT()` object, it reads predefined files containing the System Prompts (like instructions) and Exemplars (like examples) for each paradigm in every supported language.
2.  **Storage:** It stores these prompts and examples in memory (like putting tools in easily accessible drawers).
3.  **Request:** When you ask for a specific prompt (using `get_system_prompt`) or formatted context (using `get_initialized_context`), SoT quickly retrieves the correct information from its storage based on the paradigm name and language code you provide.

Here's a visual representation:

```mermaid
sequenceDiagram
    participant User
    participant SoT_Object as SoT()
    participant InternalCache as In-Memory Storage

    User->>SoT_Object: Initialize SoT()
    SoT_Object->>InternalCache: Load Prompts & Exemplars from files
    Note over SoT_Object, InternalCache: Startup Loading

    User->>SoT_Object: sot.get_system_prompt("conceptual_chaining", "EN")
    SoT_Object->>InternalCache: Fetch 'EN' prompt for 'conceptual_chaining'
    InternalCache-->>SoT_Object: Return stored prompt text
    SoT_Object-->>User: Provide prompt text

    User->>SoT_Object: sot.get_initialized_context("chunked_symbolism", "EN", format="raw")
    SoT_Object->>InternalCache: Fetch 'EN' exemplars for 'chunked_symbolism'
    InternalCache-->>SoT_Object: Return stored examples
    SoT_Object-->>User: Provide raw examples list
end
```

**Code Glimpse:**

Inside the `SoT` class, the initialization (`__init__`) sets up paths to where the prompts and exemplars are stored:

```python
# Inside sketch_of_thought/sketch_of_thought.py (simplified)
class SoT:
    def __init__(self):
        # ... other setup ...
        
        # Define where to find paradigm instructions (prompts)
        self.__PROMPT_PATH_BASE = os.path.join(str(default_path()), "config/prompts/")
        # Define where to find paradigm examples (exemplars)
        self.__CONTEXT_PATH_BASE = os.path.join(str(default_path()), "config/exemplars.json")
        
        # Map paradigm names to their specific prompt filenames
        self.__PROMPT_FILENAMES = {
            "chunked_symbolism": "ChunkedSymbolism_SystemPrompt.md",
            "expert_lexicons": "ExpertLexicons_SystemPrompt.md",
            "conceptual_chaining": "ConceptualChaining_SystemPrompt.md",
        }

        # Caches to hold loaded data
        self.PROMPT_CACHE = {}
        self.CONTEXT_CACHE = {}
        
        # Load data immediately
        self.__preload_contexts() # Reads exemplars.json
        self.__LANGUAGE_CODES = list(self.CONTEXT_CACHE.keys()) # Finds supported languages ('EN', 'KR', etc.)
        self.__preload_prompts() # Reads prompt files for each language/paradigm
```

The `__preload_prompts` and `__preload_contexts` methods (called during `__init__`) are responsible for reading the files and storing their content in `self.PROMPT_CACHE` and `self.CONTEXT_CACHE`.

When you call `get_system_prompt`:

```python
# Inside sketch_of_thought/sketch_of_thought.py (simplified)
    def get_system_prompt(self, paradigm="chunked_symbolism", language_code="EN"):
        # Basic checks (omitted for brevity) ...
        
        # Retrieve the preloaded prompt from the cache
        return copy.deepcopy(self.PROMPT_CACHE[language_code][paradigm])
```

It simply looks up the requested prompt in the `PROMPT_CACHE` dictionary using the language and paradigm name. `get_initialized_context` works similarly, accessing `CONTEXT_CACHE`. This preloading makes accessing the paradigm information very fast!

## Conclusion

In this chapter, we introduced the core concept of **Reasoning Paradigms** in SoT. We learned that these are like specialized thinking tools:

*   **Conceptual Chaining:** For linking ideas and commonsense reasoning.
*   **Chunked Symbolism:** For structured math and symbolic problems.
*   **Expert Lexicons:** For dense, technical information using jargon and symbols.

We saw how SoT defines these paradigms through specific instructions (System Prompts) and examples (Exemplars), and how you can access them using simple functions like `avaliable_paradigms`, `get_system_prompt`, and `get_initialized_context`.

Now that we understand *what* these different thinking styles are, how does SoT actually use them to process a question and generate a concise answer? The next chapter, [SoT Orchestrator](02_sot_orchestrator_.md), will show us how these paradigms are put into action.

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)