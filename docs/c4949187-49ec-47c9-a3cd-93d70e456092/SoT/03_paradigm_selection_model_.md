# Chapter 3: Paradigm Selection Model

In the [previous chapter](02_sot_orchestrator_.md), we learned about the `SoT` class, our main **Orchestrator**, which coordinates the entire reasoning process. We saw how it can take a question and prepare the necessary context (instructions and examples) for a language model. But a key step was mentioned: automatically deciding *which* [Reasoning Paradigm](01_reasoning_paradigms_.md) (Conceptual Chaining, Chunked Symbolism, or Expert Lexicons) is the best fit for the question.

How does the Orchestrator make this crucial decision? It doesn't just guess! It uses a specialized helper: the **Paradigm Selection Model**.

## The Helpful Receptionist

Imagine you walk into a very large, specialized company (like SoT) with a specific request (your question). Instead of wandering around trying to find the right department, there's a knowledgeable receptionist at the front desk. You tell them your problem, and they instantly know which department (Reasoning Paradigm) is best equipped to handle it – the math experts, the concept linkers, or the technical jargon team.

The **Paradigm Selection Model** is exactly like that receptionist. It's a small, efficient machine learning model whose only job is to look at your question and quickly predict the most suitable reasoning paradigm. This automation is super helpful because:

*   **It's Fast:** It makes the decision in a fraction of a second.
*   **It's Smart:** It's been trained on many examples to recognize patterns in questions.
*   **It's Automatic:** You don't have to figure out the best paradigm yourself!

This model is built using a technique called "fine-tuning" on a base model called DistilBERT. Think of DistilBERT as a general-purpose text understander, and we've given it special training *just* for this task of sorting questions into SoT's paradigm categories.

## How the Orchestrator Uses the Selector

You don't interact with the Paradigm Selection Model directly. The [SoT Orchestrator](02_sot_orchestrator_.md) (the `SoT` class) keeps this model tucked away inside and uses it whenever you call the `classify_question` method.

Let's revisit the example from the previous chapter:

```python
# First, create the SoT orchestrator
from sketch_of_thought import SoT
sot = SoT()

# Your question
question = "If a train travels at 60 mph for 3 hours, how far does it travel?"

# Ask the orchestrator to classify it
# This uses the Paradigm Selection Model internally!
chosen_paradigm = sot.classify_question(question)

print(f"Question: '{question}'")
print(f"Best Paradigm: {chosen_paradigm}") 
```

*Output:*

```
Question: 'If a train travels at 60 mph for 3 hours, how far does it travel?'
Best Paradigm: chunked_symbolism
```

When you call `sot.classify_question(question)`, the orchestrator passes the question to its internal Paradigm Selection Model. The model analyzes the text ("travels," "60 mph," "3 hours," "how far") and predicts that `chunked_symbolism` is the best fit because the question involves numbers and calculation. The orchestrator then returns this prediction to you.

Let's try another one:

```python
# A different type of question
question_2 = "What happens if you leave milk out of the fridge for too long?"

# Classify this one
chosen_paradigm_2 = sot.classify_question(question_2)

print(f"\nQuestion: '{question_2}'")
print(f"Best Paradigm: {chosen_paradigm_2}")
```

*Output:*

```
Question: 'What happens if you leave milk out of the fridge for too long?'
Best Paradigm: conceptual_chaining
```

Here, the model recognized that the question is about cause and effect and everyday concepts (milk, fridge, leaving out, happens), so it predicted `conceptual_chaining` as the most suitable paradigm.

## Under the Hood: A Peek Inside `classify_question`

What actually happens when `sot.classify_question()` is called? It's a quick, four-step process:

1.  **Tokenize:** The question text (like "How far does the train travel...") is converted into a sequence of numbers that the machine learning model can understand. This is done by a "tokenizer" specifically matched to the model.
2.  **Predict:** These numbers are fed into the pre-loaded Paradigm Selection Model (the fine-tuned DistilBERT). The model processes the numbers and outputs scores for each possible paradigm.
3.  **Select:** The paradigm with the highest score is chosen as the prediction. The model outputs this choice as a number (e.g., 0, 1, or 2).
4.  **Map to Name:** The orchestrator looks up this number in a simple table (a dictionary) to get the human-readable name of the paradigm (e.g., 0 might map to `chunked_symbolism`, 1 to `conceptual_chaining`, etc.). This name is then returned.

Here's a visual representation:

```mermaid
sequenceDiagram
    participant User
    participant Orchestrator as SoT()
    participant Tokenizer
    participant SelectorModel as Paradigm Selection Model (DistilBERT)
    participant Mapping as Index-to-Name Map

    User->>Orchestrator: classify_question("Train speed?")
    Orchestrator->>Tokenizer: Convert "Train speed?" to numbers
    Tokenizer-->>Orchestrator: Return numerical sequence
    Orchestrator->>SelectorModel: Process numerical sequence
    SelectorModel-->>Orchestrator: Predict class index (e.g., 0)
    Orchestrator->>Mapping: What name corresponds to index 0?
    Mapping-->>Orchestrator: Return "chunked_symbolism"
    Orchestrator-->>User: Return "chunked_symbolism"
end
```

**Code Glimpse:**

How is this implemented in the `SoT` class?

*   **Loading the Model (in `__init__`)**: When you create the `SoT()` object, it automatically downloads and loads the Paradigm Selection Model and its tokenizer from Hugging Face (a popular site for sharing ML models).

    ```python
    # Inside sketch_of_thought/sketch_of_thought.py (simplified __init__)
    from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
    import json
    import os
    from .config.config import default_path

    class SoT:
        def __init__(self):
            # Define where to get the model from
            self.__MODEL_PATH = "saytes/SoT_DistilBERT" 
            
            # Load the pre-trained model
            self.model = DistilBertForSequenceClassification.from_pretrained(self.__MODEL_PATH)
            # Load the matching tokenizer
            self.tokenizer = DistilBertTokenizer.from_pretrained(self.__MODEL_PATH)
            
            # Load the mapping from number (model output) to name (paradigm)
            self.__LABEL_MAPPING_PATH = os.path.join(str(default_path()), "config/label_mapping.json")
            self.__LABEL_MAPPING = json.load(open(self.__LABEL_MAPPING_PATH))
            
            # ... other initialization like loading prompts and examples ...
    ```
    This setup ensures the "receptionist" (model and tokenizer) is ready as soon as the SoT orchestrator starts.

*   **Using the Model (in `classify_question`)**: The `classify_question` method performs the steps we described: tokenize, predict, select, and map.

    ```python
    # Inside sketch_of_thought/sketch_of_thought.py (simplified classify_question)
    import torch # PyTorch is used by the Transformers library

    class SoT:
        # ... (init method shown above) ...

        def classify_question(self, question):
            # Step 1: Tokenize the input question text
            inputs = self.tokenizer(question, return_tensors="pt", 
                                    truncation=True, padding=True)
            
            # Step 2: Get predictions from the loaded model
            outputs = self.model(**inputs)
            
            # Step 3: Select the class index with the highest score
            predicted_class_index = torch.argmax(outputs.logits, dim=1).item() 
            
            # Step 4: Map the index (e.g., 0) to the name (e.g., "chunked_symbolism")
            # Need to reverse the mapping loaded in __init__
            label_mapping_reverse = {v: k for k, v in self.__LABEL_MAPPING.items()}
            return label_mapping_reverse[predicted_class_index]
    ```
    This method efficiently uses the pre-loaded components to classify the question.

## Conclusion

In this chapter, we zoomed in on the **Paradigm Selection Model**, the automatic "receptionist" within the [SoT Orchestrator](02_sot_orchestrator_.md). We learned:

*   It's a fine-tuned DistilBERT model specifically trained to categorize questions into SoT's reasoning paradigms.
*   It's used internally by the `sot.classify_question()` method.
*   It works by tokenizing the question, getting a prediction from the model, and mapping the result to a paradigm name (`conceptual_chaining`, `chunked_symbolism`, or `expert_lexicons`).
*   This automation saves you from having to manually choose the best reasoning style for each question.

Now that we know how SoT selects the right paradigm and gathers the basic instructions (System Prompts) and examples, how does it actually format all this information perfectly so that a large language model can understand it?

The next chapter, [Context Initialization & Formatting](04_context_initialization___formatting_.md), will explore how the `get_initialized_context` method prepares the final package for the LLM.

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)