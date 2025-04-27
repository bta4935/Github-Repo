# Chapter 2: SoT Orchestrator

In the [previous chapter](01_reasoning_paradigms_.md), we learned about the different specialized thinking tools, or **Reasoning Paradigms**, that Sketch-of-Thought (SoT) uses: Conceptual Chaining, Chunked Symbolism, and Expert Lexicons. We saw how SoT stores the instructions (System Prompts) and examples (Exemplars) for each.

But having a toolbox is one thing; knowing *how* and *when* to use each tool is another! How does SoT actually take your question, pick the right paradigm, grab the necessary instructions, and prepare everything for the language model to generate a concise answer?

This is where the **SoT Orchestrator** comes in.

## The Conductor of the Reasoning Orchestra

Think of the SoT library as an orchestra aiming to perform a beautiful piece of reasoning efficiently. The different paradigms are like sections of the orchestra (strings, woodwinds, brass). To make beautiful music together, they need a conductor.

The **SoT Orchestrator** is that conductor. It's the main engine of the library, represented by the `SoT` class in Python. It doesn't do the *final* thinking itself (that's the job of the large language model you connect it to), but it coordinates everything leading up to it:

1.  **Selects the Musicians:** It figures out which Reasoning Paradigm (musician section) is best suited for the input question.
2.  **Distributes the Sheet Music:** It fetches the correct [System Prompts](05_system_prompts_.md) (instructions) and example data (practice pieces) for the chosen paradigm.
3.  **Sets the Stage:** It organizes this information into a format ready for the language model (the performer).

Essentially, the `SoT` class is your main entry point for using the library. It brings all the pieces together.

## Getting Started: Meeting the Orchestrator

Using the SoT Orchestrator is incredibly simple. You just need to create an instance of the `SoT` class:

```python
# Import the main class from the library
from sketch_of_thought import SoT

# Create the orchestrator object!
sot = SoT() 

print("SoT Orchestrator is ready!") 
```

*Output:*

```
SoT Orchestrator is ready!
```

That's it! When you run `sot = SoT()`, the orchestrator springs to life. Behind the scenes, it loads several important things:

*   The small, specialized model used for choosing the right paradigm (the [Paradigm Selection Model](03_paradigm_selection_model_.md)).
*   All the [System Prompts](05_system_prompts_.md) for each paradigm and language.
*   All the example data (Exemplars) for each paradigm and language.

It keeps all this ready in memory, so it can work quickly when you ask it to do something.

## The Orchestrator's Main Tasks

Let's walk through the main steps the `SoT` orchestrator performs to handle a question. Imagine you want to ask: "If a train travels at 60 mph for 3 hours, how far does it travel?"

**1. Choosing the Right Tool (Paradigm Selection)**

First, the orchestrator needs to decide which reasoning style is best for this question. Is it about linking concepts, using math symbols, or technical jargon? This looks like a math problem, so "Chunked Symbolism" seems appropriate.

The orchestrator uses its built-in [Paradigm Selection Model](03_paradigm_selection_model_.md) to make this choice automatically. You can ask it to classify your question using the `classify_question` method:

```python
# Our question
question = "If a train travels at 60 mph for 3 hours, how far does it travel?"

# Ask the orchestrator to choose the best paradigm
chosen_paradigm = sot.classify_question(question)

print(f"The orchestrator chose: {chosen_paradigm}")
```

*Output:*

```
The orchestrator chose: chunked_symbolism 
```

Perfect! The orchestrator correctly identified this as a task for the "Chunked Symbolism" paradigm.

**2. Getting the Instructions and Examples (Context Preparation)**

Now that the orchestrator knows *which* paradigm to use (`chunked_symbolism`), it needs to gather the right "sheet music" for the language model. This includes:

*   The specific [System Prompt](05_system_prompts_.md) for Chunked Symbolism (telling the model *how* to think symbolically).
*   Relevant examples (Exemplars) showing the desired input/output format for math problems.
*   Your actual question.

The orchestrator does this with the `get_initialized_context` method. We tell it the paradigm we want (the one chosen in the previous step), our question, and the format we need (usually `"llm"` for standard language models).

```python
# Get the context, including system prompt and examples, for our question
context_messages = sot.get_initialized_context(
    paradigm=chosen_paradigm,  # Use the paradigm decided earlier
    question=question,         # Include our specific question
    format="llm",              # Format for a standard language model
    include_system_prompt=True # Yes, include the instructions
)

# Let's peek at the structure and the last message (our question)
print(f"Context format: {type(context_messages)}")
print(f"Number of messages prepared: {len(context_messages)}")
print(f"Last message: {context_messages[-1]}") 
```

*Output:*

```
Context format: <class 'list'>
Number of messages prepared: 6 # System Prompt + 2 Example Pairs + Our Question
Last message: {'role': 'user', 'content': 'If a train travels at 60 mph for 3 hours, how far does it travel?'}
```

The orchestrator has prepared a list of messages. This list starts with the system prompt for Chunked Symbolism, followed by a few examples of Chunked Symbolism in action, and finally, includes our specific question. This list is now perfectly formatted to be sent to a compatible large language model (like GPT, Llama, Mistral, Qwen etc.).

**3. Ready for the Performance**

The `SoT` orchestrator's job is now mostly done. It has:

*   Analyzed the question.
*   Selected the best reasoning paradigm (`chunked_symbolism`).
*   Prepared the necessary instructions and examples (`context_messages`).

The `context_messages` list is the final output *from the orchestrator*. You would now typically pass this list to your chosen language model to generate the actual step-by-step reasoning and the final answer, using the efficient SoT style guided by the prompt and examples. (The SoT library itself doesn't include the LLM, but prepares everything for it).

## Under the Hood: How the Orchestrator Works

Let's briefly look inside the `SoT` class to understand how it manages these tasks.

**Initialization (`__init__`)**

When you create the `SoT()` object, the `__init__` method gets busy:

1.  **Loads the Selector:** It loads the pre-trained [Paradigm Selection Model](03_paradigm_selection_model_.md) (a lightweight DistilBERT model) and its tokenizer. This model is small and fast, designed specifically to categorize questions into the SoT paradigms.
2.  **Loads Prompts & Exemplars:** As we saw in Chapter 1, it reads all the `.md` prompt files and the `exemplars.json` file into memory (`PROMPT_CACHE` and `CONTEXT_CACHE`). This makes accessing them later very quick.

**Classification (`classify_question`)**

When you call `sot.classify_question(your_question)`:

1.  **Tokenize:** It uses the loaded tokenizer to convert your question text into numbers the model understands.
2.  **Predict:** It feeds these numbers to the loaded DistilBERT model.
3.  **Get Label:** The model outputs a prediction (e.g., class `0`, `1`, or `2`).
4.  **Map to Name:** It looks up this number in a mapping to get the human-readable paradigm name (e.g., `chunked_symbolism`).

**Context Preparation (`get_initialized_context`)**

When you call `sot.get_initialized_context(...)`:

1.  **Lookup:** It uses the provided `paradigm` name and `language_code` to find the correct [System Prompt](05_system_prompts_.md) and list of examples (Exemplars) in its pre-loaded caches (`PROMPT_CACHE` and `CONTEXT_CACHE`).
2.  **Format:** It arranges the system prompt (if requested), the examples, and your question into the specified `format` (like the `"llm"` list of dictionaries).

Here’s a simplified sequence diagram showing the flow for getting the context ready:

```mermaid
sequenceDiagram
    participant User
    participant Orchestrator as SoT()
    participant Selector as Paradigm Selection Model
    participant Cache as In-Memory Prompts/Examples

    User->>Orchestrator: question = "Train speed..."
    User->>Orchestrator: classify_question(question)
    Orchestrator->>Selector: Process question text
    Selector-->>Orchestrator: Predicted paradigm = "chunked_symbolism"
    Orchestrator-->>User: Return "chunked_symbolism"

    User->>Orchestrator: get_initialized_context(paradigm="chunked_symbolism", question=question, format="llm")
    Orchestrator->>Cache: Request "chunked_symbolism" prompt (EN)
    Cache-->>Orchestrator: Return prompt text
    Orchestrator->>Cache: Request "chunked_symbolism" examples (EN)
    Cache-->>Orchestrator: Return example list
    Note right of Orchestrator: Format prompt, examples, and question into 'llm' structure
    Orchestrator-->>User: Return formatted context_messages list
end
```

**Code Glimpse:**

Let's look at simplified snippets from `sketch_of_thought/sketch_of_thought.py`:

*   **Initialization (`__init__`)**:
    ```python
    # Inside the SoT class __init__ method (simplified)
    def __init__(self):
        # Load the classification model and tokenizer
        self.__MODEL_PATH = "saytes/SoT_DistilBERT" 
        self.model = DistilBertForSequenceClassification.from_pretrained(self.__MODEL_PATH)
        self.tokenizer = DistilBertTokenizer.from_pretrained(self.__MODEL_PATH)
        
        # Load mapping from model output (numbers) to paradigm names (text)
        self.__LABEL_MAPPING_PATH = os.path.join(str(default_path()), "config/label_mapping.json")
        self.__LABEL_MAPPING = json.load(open(self.__LABEL_MAPPING_PATH))
        
        # Set paths for prompts and examples
        self.__PROMPT_PATH_BASE = os.path.join(str(default_path()), "config/prompts/")
        self.__CONTEXT_PATH_BASE = os.path.join(str(default_path()), "config/exemplars.json")

        # Prepare caches to store loaded data
        self.PROMPT_CACHE = {}
        self.CONTEXT_CACHE = {}
        
        # Load prompts and examples into the caches immediately
        self.__preload_contexts() 
        self.__LANGUAGE_CODES = list(self.CONTEXT_CACHE.keys())
        self.__preload_prompts()
        # ... rest of init ...
    ```
    This sets up the orchestrator by loading the necessary models and data files right at the start.

*   **Classification (`classify_question`)**:
    ```python
    # Inside the SoT class (simplified)
    def classify_question(self, question):
        # Convert question text to model inputs
        inputs = self.tokenizer(question, return_tensors="pt", truncation=True, padding=True)
        
        # Get prediction from the model
        outputs = self.model(**inputs)
        predicted_class = torch.argmax(outputs.logits, dim=1).item() # Get the winning class index (e.g., 0, 1, 2)
        
        # Map the index back to the paradigm name (e.g., 'chunked_symbolism')
        label_mapping_reverse = {v: k for k, v in self.__LABEL_MAPPING.items()}
        return label_mapping_reverse[predicted_class]
    ```
    This shows how the orchestrator uses the loaded model and tokenizer to pick the best paradigm for a given question.

The `get_initialized_context` method (not shown here for brevity, but covered conceptually in Chapter 1 and above) primarily accesses the `PROMPT_CACHE` and `CONTEXT_CACHE` that were filled during `__init__`.

## Conclusion

In this chapter, we met the **SoT Orchestrator**, the central `SoT` class that acts like the conductor of our reasoning orchestra. We learned that its main job is to coordinate the reasoning process by:

1.  Loading all necessary components (selection model, prompts, examples) when initialized.
2.  Automatically selecting the best [Reasoning Paradigm](01_reasoning_paradigms_.md) for a given question using `classify_question`.
3.  Fetching the corresponding [System Prompt](05_system_prompts_.md) and examples, and formatting them along with the user's question using `get_initialized_context`.
4.  Providing a ready-to-use context for a large language model to perform the final, efficient reasoning steps.

The `SoT` orchestrator simplifies the process, allowing you to easily leverage the power of different reasoning styles without needing to manage all the details yourself.

But how exactly does that automatic selection in `classify_question` work? What's inside that little model? In the next chapter, we'll dive deeper into the [Paradigm Selection Model](03_paradigm_selection_model_.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)