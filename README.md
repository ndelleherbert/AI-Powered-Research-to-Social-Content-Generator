# \# 🚀 AI-Powered Research-to-Social Content Generator

# 

# > Turns any topic into a research report + LinkedIn, Facebook \& Instagram posts using Claude AI and LangChain.

# 

# \---

# 

# \## 📌 Overview

# 

# A Streamlit web app that automates the full content pipeline:

# 

# \*\*Topic → Research Report → 5-Bullet Summary → Social Media Posts\*\*

# 

# Powered by \*\*Anthropic Claude\*\* (`claude-sonnet-4-5`) and \*\*LangChain\*\*, with all three social posts generated simultaneously using `RunnableParallel`.

# 

# \---

# 

# \## ✨ Features

# 

# \- 📄 \*\*Research Report\*\* — detailed, structured report with headings and sections

# \- 🔍 \*\*5-Bullet Summary\*\* — key insights distilled from the report

# \- 📣 \*\*3 Platform Posts\*\* generated in parallel:

# &#x20; - 🔗 \*\*LinkedIn\*\* — 120–180 words, hook, tip, question, hashtags

# &#x20; - 📘 \*\*Facebook\*\* — conversational, community-focused, call-to-action

# &#x20; - 📸 \*\*Instagram\*\* — punchy caption with emojis and hashtags

# 

# \---

# 

# \## 🛠️ Tech Stack

# 

# | Layer | Tool |

# |---|---|

# | Frontend | Streamlit |

# | LLM | Anthropic Claude (`claude-sonnet-4-5`) |

# | Orchestration | LangChain |

# | Prompting | `PromptTemplate` |

# | Output Parsing | `StrOutputParser` |

# | Parallel Execution | `RunnableParallel` |

# 

# \---

# 

# \## ⚙️ Setup \& Installation

# 

# \### 1. Clone the repository

# ```bash

# git clone https://github.com/YOUR\_USERNAME/AI-Powered-Research-to-Social-Content-Generator.git

# cd AI-Powered-Research-to-Social-Content-Generator

# ```

# 

# \### 2. Create and activate a virtual environment

# ```bash

# python -m venv myenv

# 

# \# Windows

# myenv\\Scripts\\activate

# 

# \# macOS / Linux

# source myenv/bin/activate

# ```

# 

# \### 3. Install dependencies

# ```bash

# pip install -r requirements.txt

# ```

# 

# \### 4. Set your Anthropic API key

# 

# \*\*Option A — Streamlit secrets\*\* (recommended):

# 

# Create `.streamlit/secrets.toml`:

# ```toml

# ANTHROPIC\_API\_KEY = "sk-ant-your-key-here"

# ```

# 

# \*\*Option B — Environment variable\*\*:

# ```bash

# \# Windows

# set ANTHROPIC\_API\_KEY=sk-ant-your-key-here

# 

# \# macOS / Linux

# export ANTHROPIC\_API\_KEY=sk-ant-your-key-here

# ```

# 

# \### 5. Run the app

# ```bash

# streamlit run app.py

# ```

# 

# \---

# 

# \## 🗂️ Project Structure

# 

# ```

# ├── app.py                  # Main Streamlit application

# ├── requirements.txt        # Python dependencies

# ├── .gitignore              # Excludes secrets and venv

# ├── .streamlit/

# │   └── secrets.toml        # API key (not committed)

# └── README.md

# ```

# 

# \---

# 

# \## 🔄 Pipeline Architecture

# 

# ```

# User Input (Topic)

# &#x20;      │

# &#x20;      ▼

# &#x20; Chain 1: Research Report

# &#x20; (PromptTemplate → Claude → StrOutputParser)

# &#x20;      │

# &#x20;      ▼

# &#x20; Chain 2: 5-Bullet Summary

# &#x20; (PromptTemplate → Claude → StrOutputParser)

# &#x20;      │

# &#x20;      ▼

# &#x20; RunnableParallel

# &#x20; ┌────────────┬────────────┬─────────────┐

# &#x20; ▼            ▼            ▼

# LinkedIn     Facebook    Instagram

# &#x20; Post         Post         Post

# ```

# 

# \---

# 

# \## 🚀 Deploy on Streamlit Cloud

# 

# 1\. Push your code to GitHub (without `secrets.toml`)

# 2\. Go to \[share.streamlit.io](https://share.streamlit.io)

# 3\. Connect your repository

# 4\. Add `ANTHROPIC\_API\_KEY` under \*\*App Settings → Secrets\*\*

# 5\. Click \*\*Deploy\*\*

# 

# \---

# 

# \## ⚠️ Security Notes

# 

# \- Never commit your `.env` or `secrets.toml` file

# \- Always add them to `.gitignore`

# \- If a key is accidentally exposed, revoke it immediately at \[console.anthropic.com](https://console.anthropic.com)

# 

# \---

# 

# \## 📄 License

# 

# MIT License — free to use, modify, and distribute.

