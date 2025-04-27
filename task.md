
# 1. IdentifyAbstractions Node
Purpose: Ask the LLM to identify the most important abstractions in the codebase.

Prompt Template (lines ~109–143):

python
CopyInsert
prompt = f"""
For the project `{project_name}`:

Codebase Context:
{context}

{language_instruction}Analyze the codebase context.
Identify the top 5-10 core most important abstractions to help those new to the codebase.

For each abstraction, provide:
1. A concise `name`{name_lang_hint}.
2. A beginner-friendly `description` explaining what it is with a simple analogy, in around 100 words{desc_lang_hint}.
3. A list of relevant `file_indices` (integers) using the format `idx # path/comment`.

List of file indices and paths present in the context:
{file_listing_for_prompt}

Format the output as a YAML list of dictionaries:
...
"""

# 2. AnalyzeRelationships Node
Purpose: Instruct the LLM to summarize the project and describe relationships between abstractions.

Prompt Template (lines ~248–269):

python
CopyInsert
prompt = f"""
Based on the following abstractions and relevant code snippets from the project `{project_name}`:

List of Abstraction Indices and Names{list_lang_note}:
{abstraction_listing}

Context (Abstractions, Descriptions, Code):
{context}

{language_instruction}Please provide:
1. A high-level `summary` of the project's main purpose and functionality in a few beginner-friendly sentences{lang_hint}. Use markdown formatting with **bold** and *italic* text to highlight important concepts.
2. A list (`relationships`) describing the key interactions between these abstractions. For each relationship, specify:
    - `from_abstraction`: Index of the source abstraction (e.g., `0 # AbstractionName1`)
    - `to_abstraction`: Index of the target abstraction (e.g., `1 # AbstractionName2`)
    - `label`: A brief label for the interaction **in just a few words**{lang_hint} (e.g., "Manages", "Inherits", "Uses").
    Ideally the relationship should be backed by one abstraction calling or passing parameters to another.
    Simplify the relationship and exclude those non-important ones.

IMPORTANT: Make sure EVERY abstraction is involved in at least ONE relationship (either as source or target). Each abstraction index must appear at least once across all relationships.

Format the output as YAML:
"""

# 3. OrderChapters Node
Purpose: Ask the LLM to determine the best order for tutorial chapters.

Prompt Template
(Based on your previous reveal around line 395, not shown in full, but structure is similar):

python
CopyInsert
prompt = f"""
Given the following abstractions and their relationships, determine the most logical order to present them as tutorial chapters for someone new to the codebase.

List of Abstractions:
{abstractions}

Relationships:
{relationships}

Please return a YAML list of abstraction indices in the recommended order.
"""

# 4. WriteChapters Node
Purpose: Instruct the LLM to generate the content for each tutorial chapter.

Prompt Template
(Not revealed, but typically structured as):

python
CopyInsert
prompt = f"""
Write a detailed, beginner-friendly tutorial chapter for the following abstraction in the project `{project_name}`.

Abstraction:
{name}
Description:
{description}
Relevant Code:
{code_snippets}

Format the output as Markdown.
"""

# 5. If you want the exact prompt template for any specific node (e.g., WriteChapters, CombineTutorial) or want to see the full code for those sections, let me know which lines or node to display and I’ll extract the prompt for you!