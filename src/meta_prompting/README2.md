# 🧠 Meta Prompting Framework

Meta Prompting is a technique that takes an initial prompt and improves it using a higher-level prompt (called a "meta prompt"). This repository demonstrates how to generate optimized prompts using an LLM (e.g., GPT-4) with a focus on enhancing clarity, structure, and task effectiveness.

---

## 📌 What is Meta Prompting?

Meta Prompting uses a higher-level prompt to **refine or improve** another prompt. This allows:
- Better clarity and task structure
- Improved LLM output quality
- Automation of prompt design

---

## 🖼️ Flow Diagram

![Meta Prompting Flowchart](meta_prompting_flowchart.png)

---

## 🧪 Example Meta Prompt

```python
meta_prompt = """
Improve the following prompt to generate a more detailed summary. 
Adhere to prompt engineering best practices. 
Make sure the structure is clear and intuitive and contains the type of news, tags and sentiment analysis.

{simple_prompt}

Only return the prompt.
"""
```

---

## 🎯 Sample Scenario

### ✅ Input Prompt

```python
simple_prompt = "Summarize the news article."
```

### ✅ Output After Meta Prompting

```
Summarize the news article with the following requirements:
1. Identify the main topic and type of news (e.g., political, economic, technology, sports, etc.).
2. Provide 3–5 keyword tags relevant to the content.
3. Perform a basic sentiment analysis (positive, neutral, or negative).
4. Ensure the summary is clear, concise, and covers all critical details.
```

---

## 💡 Additional Prompt Scenarios

Here are more situations where meta prompting can be applied:

---

### 🎨 Creative Writing Prompt

```python
meta_prompt = """
Refine the following prompt to inspire a short story idea.
Make it more imaginative, include a unique setting, a main character, and a central conflict.

{simple_prompt}

Only return the prompt.
"""
```

---

### 🔍 Research Assistance

```python
meta_prompt = """
Improve the following research question to make it more specific, measurable, and aligned with academic standards.
Ensure clarity and avoid ambiguity.

{simple_prompt}

Only return the prompt.
"""
```

---

## 🚀 How to Run

You can use this with any LLM (like OpenAI's GPT or a local model). Here's a simple example using `openai` Python SDK.

```python
import openai

def apply_meta_prompt(meta_prompt: str, simple_prompt: str) -> str:
    final_prompt = meta_prompt.format(simple_prompt=simple_prompt)
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": final_prompt}]
    )
    
    return response['choices'][0]['message']['content'].strip()

# Example usage:
meta_prompt = """..."""  # Replace with one of the meta prompts above
simple_prompt = "Summarize the news article."
print(apply_meta_prompt(meta_prompt, simple_prompt))
```

---

## 📂 File Structure

```
meta_prompting/
│
├── meta_prompting_flowchart.png  # Visual guide for meta prompting logic
├── README.md                     # You're here!
└── main.py                       # (Optional) Script to run examples
```

---

## 🙋‍♂️ Why Use This?

- Automate prompt engineering
- Build better interfaces for non-technical users
- Boost performance of your LLM applications

---

## 🧠 Tip

Experiment with multiple prompt types and try chaining meta prompts for even deeper refinement!

---

## 📜 License

MIT License. Use freely with attribution.

---

## 👤 Author

Made with ❤️ by [Your Name]
