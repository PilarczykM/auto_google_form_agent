# AutoGF-Agent

AutoGF-Agent is a CLI-based application that uses an AI agent with a customizable personality to automatically fill out **public Google Forms**. Built with **CrewAI** and **Playwright**, it simulates natural, personality-driven responses and includes an optional supervisor agent to evaluate answer quality.

---

## 🚀 Features

- Fills out **public** Google Forms (no login required).
- Supports multiple question types: text fields, multiple choice, scales.
- Personality-aware responses based on user-defined traits.
- Optional response evaluation and correction via a Supervisor Agent.
- Simple CLI interface.

---

## 🧠 How It Works

1. **User** runs the CLI with:
   - Language (`--lang`)
   - Personality traits (`--personality`)
   - Google Form URL (`--form-url`)
   - Optional quality check (`--enforce-quality-check`)

2. **FormAgent** (CrewAI) generates responses according to personality and language.

3. **Playwright** opens the Google Form and fills in the answers.

4. **SupervisorAgent** evaluates the responses (optional):
   - Checks stylistic coherence and quality.
   - Provides a rating and comments.
   - Optionally regenerates or fixes answers.

5. **Output** includes:
   - Completed Google Form
   - CLI feedback
   - Quality report (if enabled)

---

## 🛠️ Requirements

- Python 3.10+
- Dependencies:
  - `playwright`
  - `crewai`
  - `click`
  - `beautifulsoup4`
  - `rich`

---

## 🧪 Example Usage

```bash
python main.py \
  --lang en \
  --personality "formal, polite, concise" \
  --form-url "https://docs.google.com/forms/..." \
  --enforce-quality-check
```

---

## ⚠️ Limitations (MVP)

- Only supports public Google Forms (no authentication).
- Does not support file uploads or custom components.
- Personality affects tone and style, not factual correctness.
- SupervisorAgent cannot directly edit forms—only suggests or triggers re-generation.

---

## 🚧 TODO — Remaining Features

### ✅ Completed
- [x] CLI interface: language, personality, form URL, quality check flag  
- [x] Question extraction using Playwright  
- [x] Per-question screenshots  
- [x] File name sanitization utility (`sanitize_filename`)  
- [x] Screenshot directory management with cleanup (`reset_screenshot_dir`)  

---

### 🛠️ In Progress / Next Steps

#### 🧠 FormAgent
- [ ] Design `FormAgent` class:
  - [ ] Accept `lang` and `personality` traits
  - [ ] Method: `generate_answers(questions) -> dict[question_text, answer]`
- [ ] Generate responses based on question text (and optionally screenshots)

#### 🧪 SupervisorAgent
- [ ] Implement `SupervisorAgent.review(questions, answers)`:
  - [ ] Score responses (0–10)
  - [ ] Add feedback/comments
  - [ ] Optionally revise weak responses
  - [ ] Return `final_answers` dictionary

#### ✍️ FormFiller
- [ ] Reuse existing Playwright session (same `page`)
- [ ] Implement `fill_form(page, final_answers)`
  - [ ] Locate each question by text
  - [ ] Match answer and inject into appropriate input
  - [ ] Handle multiple-choice, text fields, linear scales
- [ ] Handle form sections (`Next`, `Back`, etc.)
- [ ] Submit form if applicable
