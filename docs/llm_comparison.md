# **Comparing LLMs for Code Generation**

## **Introduction**

The goal of this comparison is to evaluate how different LLMs perform when handling structured code-related prompts. We focus on three distinct configurations:

1. **Gemini-2.0-Flash** with **text-embedding-004**
2. **Gemini-2.0-Flash** with **text-embedding-3-small**
3. **OpenAI GPT-4o** with **text-embedding-3-small**

The prompts used for this evaluation are defined in `docs/prompt_examples.md` and cover a range of complexity levels. By analyzing the responses, we aim to understand how each model handles structured coding tasks, migration strategies, refactoring, and performance optimization.

---

## **Evaluation Scenarios**

We will evaluate the models based on prompts of increasing complexity. Each level tests different aspects of code understanding, reasoning, and generation. Below are the prompts and results.

---

### **Level 1: Basic Code Modifications**
**Task:** Add `created_at` and `updated_at` fields to the `User` model, including Django migrations and tests.

**Results:**

**Gemini-2.0-Flash (text-embedding-004):**  
- Model incorrectly modified; `created_at` and `updated_at` added to `UserManager` instead of `User`.
- Migrations not created.
- Tests placed incorrectly within the code.

**Gemini-2.0-Flash (text-embedding-3-small):**  
- `User` model correctly updated.
- Migrations not created.
- Tests placed incorrectly within the code.

**OpenAI GPT-4o (text-embedding-3-small):**  
- `User` model correctly updated.
- Migration correctly generated.
- Tests placed incorrectly within the code.

---

### **Level 2: Custom Model Manager Implementation**
**Task:** Implement a custom manager for filtering users with both first and last names, including tests.

**Results:**

**Gemini-2.0-Flash (text-embedding-004):**  
- Incorrectly modified custom manager.
- Tests formatted correctly but not functional.

**Gemini-2.0-Flash (text-embedding-3-small):**  
- Incorrectly modified custom manager.
- Tests placed incorrectly within the code.

**OpenAI GPT-4o (text-embedding-3-small):**  
- Custom manager correctly implemented.
- Tests placed incorrectly within the code.

---

### **Level 3: Database Migration and Field Removal**
**Task:** Remove the `user_handle` field from the `User` model, generate a migration, and update related code and tests.

**Results:**

**Gemini-2.0-Flash (text-embedding-004):**  
- Model incorrectly modified, with unintended formatting and logic changes.
- Migration incorrectly generated.
- Tests not working as expected and improperly formatted.

**Gemini-2.0-Flash (text-embedding-3-small):**  
- Model contained errors and duplicate code.
- Migration incorrectly generated.
- Tests not functioning correctly but well formatted.

**OpenAI GPT-4o (text-embedding-3-small):**  
- `user_handle` not removed.
- Migration not generated.
- Tests incorrectly formatted but correctly added test for `AttributeError`.

---

### **Level 4: Many-to-Many Relationship Implementation**
**Task:** Implement a many-to-many relationship with additional fields on the relationship.

**Results:**

**Gemini-2.0-Flash (text-embedding-004):**  
- `UserGroup` model correctly created and formatted.
- Migrations correctly generated.
- Tests not created or modified.

**Gemini-2.0-Flash (text-embedding-3-small):**  
- `UserGroup` model correctly created but poorly formatted.
- Migrations correctly generated.
- Tests not created or modified.

**OpenAI GPT-4o (text-embedding-3-small):**  
- `UserGroup` model correctly created but poorly formatted.
- Migrations correctly generated.
- Tests correctly implemented.

---

## **Comparison Table**

| Model | Embedding | Accuracy | Code Quality | Completeness | Handling Edge Cases |
|--------|---------------------------|-----------|--------------|--------------|----------------|
| Gemini-2.0-Flash | text-embedding-004 | Low | Low | Incomplete | Struggles with complex logic |
| Gemini-2.0-Flash | text-embedding-3-small | Medium | Medium | Incomplete | Handles basic changes, struggles with complex cases |
| OpenAI GPT-4o | text-embedding-3-small | Good | Good | Complete | Best at handling complex scenarios |

---

This structured comparison helps determine which combination of LLM and embedding model is the most effective for code-related tasks. Based on the evaluations, **OpenAI GPT-4o** with **text-embedding-3-small** is currently the best-performing configuration.
