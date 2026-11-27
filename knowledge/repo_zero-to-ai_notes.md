# External GitHub Repository Knowledge: zero-to-ai (https://github.com/PavanMudigonda/zero-to-ai)

## CODE_OF_CONDUCT.md
# Code of Conduct

This is a learning community. People come here from many countries, languages, backgrounds, and skill levels. We want everyone to feel welcome.

## Expected behavior

- Be patient with beginners. Everyone was new once.
- Be respectful in issues, PRs, and discussions. Disagree with ideas, not with people.
- Assume good faith. Most misunderstandings are language or context, not malice.
- Credit other people's work. Cite papers, repos, and ideas you build on.

## Unacceptable behavior

- Personal attacks, harassment, or insults — including over gender, nationality, race, religion, sexual orientation, or skill level.
- Discriminatory or demeaning language, including in code, comments, or example data.
- Publishing private information (email, phone, address) without consent.
- Spamming, off-topic promotion, or repeatedly ignoring maintainer feedback.

## Scope

This Code applies to all project spaces: issues, PRs, discussions, the GitHub repo, the website, and any official chat. It also applies when you represent the project in public.

## Reporting

If you experience or witness unacceptable behavior, report it by emailing the maintainer at **mnpawan@gmail.com**, or open a private security advisory on GitHub.

All reports are read. Reporters are not named in any response.

## Enforcement

Maintainers may, at their discretion:

- Edit or remove offending content.
- Close an issue, PR, or discussion.
- Temporarily or permanently block a user from project spaces.

We aim to be proportionate. A first-time, minor issue gets a private nudge; repeated or severe behavior gets a stronger response.

## Attribution

Adapted from the [Contributor Covenant](https://www.contributor-covenant.org/) v2.1, simplified for this project's audience.


## CONTRIBUTING.md
# Contributing to Zero to AI

Thank you for considering a contribution. This is an open-source AI/ML curriculum aimed at learners around the world, so contributions that improve **clarity, accessibility, and accuracy** are especially welcome.

You do not need to be an expert. Fixing a typo, clarifying a paragraph, or translating one notebook is a real contribution.

## Ways to Contribute

- **Fix a typo or broken link** — open a PR directly, no issue needed.
- **Report a bug** — open an [issue](https://github.com/PavanMudigonda/zero-to-ai/issues) using the bug report template.
- **Suggest a notebook or topic** — open an [issue](https://github.com/PavanMudigonda/zero-to-ai/issues) using the notebook suggestion template.
- **Improve an explanation** — open a PR with the change.
- **Add a translation** — see [Translations](#translations) below.
- **Add or improve a notebook** — please open an issue first for anything larger than a small edit, so we can align on scope.

## Repository Layout

The curriculum lives in two parallel trees, kept in sync:

- `jupyter-notebooks/<phase>/` — source of truth for runnable notebooks.
- `next-docs/src/app/<phase>/` — auto-generated MDX wrappers that render notebooks on [zero-to-ai.dev](https://zero-to-ai.dev/).

Always edit notebooks under `jupyter-notebooks/`, then run:

```bash
python3 scripts/sync_notebooks.py
python3 scripts/generate_meta_sequential.py
```

These regenerate the MDX wrappers and the Nextra sidebar.

## Setup

```bash
git clone https://github.com/<your-username>/zero-to-ai.git
cd zero-to-ai
./install_dependencies.sh
```

If you only need to edit text or docs, you can skip the install — Markdown and MDX changes don't need a Python environment.

## Tooling Config

The shared MCP configuration for this repository lives in `.mcp.json` at the repo root.

If you keep a local `.vscode/mcp.json`, treat it as editor-specific convenience config. It is ignored by git and should not become the source of truth for repository tooling.

## Making a Change

1. Create a branch: `git checkout -b fix/<short-description>`.
2. Make your change. For notebooks, **clear outputs before committing** unless the output is part of the lesson:
   ```bash
   jupyter nbconvert --clear-output --inplace <notebook>.ipynb
   ```
3. If you edited a notebook, run the sync scripts above.
4. Commit with a short, descriptive message:
   - `fix: clarify backprop step in 06-neural-networks/02_backprop`
   - `docs: add note about Kaggle phone verification in README`
   - `feat: new notebook on RAG evaluation in 08-rag`
5. Push and open a PR.

## What Makes a Good PR

- **One topic per PR.** A typo fix and a new notebook are two PRs.
- **No huge formatting reflows.** Touch only what you need to.
- **Beginner-friendly explanations.** Assume the reader is a global learner, sometimes reading in their second or third language. Avoid jargon when a plain word works.
- **Working code.** Cells should execute top-to-bottom without errors. If a cell needs an API key, mark it clearly and don't put your own key in.
- **No tracked outputs over 1 MB** unless the output is the lesson (e.g. a generated image).

## Translations

We welcome translations into any language. A few principles:

- Translate the **explanations and headings**, keep the **code** unchanged (variable names, library calls, etc.).
- Put translated notebooks alongside the original with a language suffix, e.g. `02_basic_prompting.es.ipynb` for Spanish.
- If you'd like to translate a whole phase, open an issue first so we can track the effort and avoid duplicates.

## Code of Conduct

By participating you agree to our [Code of Conduct](CODE_OF_CONDUCT.md). Be kind, be patient, and assume good faith.

## Questions?

Open a [discussion](https://github.com/PavanMudigonda/zero-to-ai/discussions) or an [issue](https://github.com/PavanMudigonda/zero-to-ai/issues). For larger ideas, drafting an issue before a PR saves everyone time.


## README.md
<!--
Keywords: machine learning course, deep learning tutorial, llm tutorial, rag tutorial, ai agents, prompt engineering, python ai, pytorch tutorial, transformers, openai api, fine-tuning, mlops, vector databases, nlp, computer vision, data science course, artificial intelligence guide, full stack ai, generative ai course, build ai applications, learn ai from scratch
-->

# Zero to AI - Free AI/ML Course: Python, LLMs, RAG, Agents & Deep Learning

Zero to AI is a free, open-source AI course and machine learning curriculum for learning Python, data science, deep learning, large language models (LLMs), retrieval-augmented generation (RAG), AI agents, prompt engineering, fine-tuning, and MLOps through 950+ hands-on Jupyter notebooks.

Use the live site for the guided learning experience at [zero-to-ai.dev](https://zero-to-ai.dev/), and use this GitHub repo as the source curriculum, notebook library, and contribution hub.

Quick links: [Website](https://zero-to-ai.dev/) • [Course Setup](https://zero-to-ai.dev/00-course-setup) • [Glossary](https://zero-to-ai.dev/23-glossary/01_GLOSSARY) • [GitHub Repo](https://github.com/PavanMudigonda/zero-to-ai)

[![GitHub license](https://img.shields.io/github/license/PavanMudigonda/zero-to-ai.svg)](https://github.com/PavanMudigonda/zero-to-ai/blob/main/LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/PavanMudigonda/zero-to-ai.svg)](https://GitHub.com/PavanMudigonda/zero-to-ai/graphs/contributors/)
[![GitHub issues](https://img.shields.io/github/issues/PavanMudigonda/zero-to-ai.svg)](https://GitHub.com/PavanMudigonda/zero-to-ai/issues/)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/PavanMudigonda/zero-to-ai.svg)](https://GitHub.com/PavanMudigonda/zero-to-ai/pulls/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

[![GitHub watchers](https://img.shields.io/github/watchers/PavanMudigonda/zero-to-ai.svg?style=social&label=Watch)](https://GitHub.com/PavanMudigonda/zero-to-ai/watchers/)
[![GitHub forks](https://img.shields.io/github/forks/PavanMudigonda/zero-to-ai.svg?style=social&label=Fork)](https://GitHub.com/PavanMudigonda/zero-to-ai/network/)
[![GitHub stars](https://img.shields.io/github/stars/PavanMudigonda/zero-to-ai.svg?style=social&label=Star)](https://GitHub.com/PavanMudigonda/zero-to-ai/stargazers/)

---

[![Open in Browser](https://img.shields.io/badge/Open%20in-Browser-F38020?style=flat&logo=cloudflare)](https://zero-to-ai.dev/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/PavanMudigonda/zero-to-ai/blob/main)
[![Open in Replit](https://img.shields.io/badge/Open%20in-Replit-blue?style=flat&logo=replit)](https://replit.com/github/PavanMudigonda/zero-to-ai)
[![Open in Kaggle](https://img.shields.io/badge/Open%20in-Kaggle-20BEFF?style=flat&logo=kaggle)](https://www.kaggle.com/code)
[![Open in SageMaker Studio Lab](https://img.shields.io/badge/Open%20in-SageMaker%20Studio%20Lab-orange?style=flat&logo=amazon-aws)](https://studiolab.sagemaker.aws/import/github/PavanMudigonda/zero-to-ai)
[![Open in Codespaces](https://img.shields.io/badge/Open%20in-Codespaces-black?style=flat&logo=github)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=PavanMudigonda/zero-to-ai)
[![github.dev](https://img.shields.io/badge/Open%20in-github.dev-black?style=flat&logo=github)](https://github.dev/PavanMudigonda/zero-to-ai)

**Click any badge above to start coding in seconds!**

---

## 📊 Course Overview

> **From Zero to AI Mastery** is still evolving. The core path is already usable, and feedback is welcome as later phases continue to grow.

This repository is best used as a guided curriculum, not as a directory to browse at random. Some phases are mature and portfolio-ready today, while a few later phases are still being filled in.

### What You'll Learn

| Area | Topics | Notebooks |
|------|--------|-----------|
| **Python & Data Science** | NumPy, Pandas, Matplotlib, Scikit-learn | 278+ |
| **Mathematics for ML** | Linear algebra, calculus, statistics, optimization | 40+ |
| **Tokenization & Embeddings** | tiktoken, SentencePiece, OpenAI, HuggingFace | 20+ |
| **Deep Learning** | Neural networks, CNNs, RNNs, Transformers from scratch | 45+ |
| **LLMs & RAG** | Retrieval-Augmented Generation, vector databases, chunking | 20+ |
| **AI Agents** | Function calling, MCP, OpenAI Agents SDK, LangGraph, multi-agent | 11+ |
| **Prompt & Context Engineering** | Chain-of-thought, structured outputs, DSPy | 6+ |
| **Fine-Tuning** | LoRA, QLoRA, PEFT, GRPO, DPO | 12+ |
| **MLOps & Serving** | Deployment, monitoring, vLLM, quantization | 15+ |
| **Evaluation & Safety** | LLM-as-judge, red teaming, bias, fairness | 12+ |
| **Advanced Topics** | GANs, VAEs, RL, causal inference, time series | 60+ |

## ✅ Start Here

The canonical reading experience is the live site at [zero-to-ai.dev](https://

## SECURITY.md
# Security Policy

Zero to AI is an educational repository made up of Jupyter notebooks, course
content, a documentation website (`next-docs/`), and Python maintenance tooling
(`scripts/`). It is not a deployed product, but we still take security seriously
for the build pipeline, dependencies, and the public documentation site at
[zero-to-ai.dev](https://zero-to-ai.dev/).

## Supported Versions

This project is rolling-release. Only the latest state of the `main` branch is
supported. Please make sure you are on the most recent commit before reporting an
issue.

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Instead, report privately using one of the following:

- Open a [GitHub Security Advisory](https://github.com/PavanMudigonda/zero-to-ai/security/advisories/new)
  (preferred), or
- Email the maintainer at **mnpawan@gmail.com** with the subject line
  `SECURITY: zero-to-ai`.

When reporting, please include:

- A description of the vulnerability and its potential impact.
- Steps to reproduce, or a proof of concept.
- The affected file(s), workflow(s), or dependency.

We aim to acknowledge new reports within a few days. Once a fix is available,
we will coordinate a disclosure timeline with you.

## Scope

In scope:

- The GitHub Actions workflows in `.github/workflows/`.
- The documentation site build and runtime in `next-docs/`.
- Python tooling in `scripts/`.
- Declared dependencies in `pyproject.toml`, `requirements*.txt`,
  `environment.yml`, and the `package.json` files.

Out of scope:

- Vulnerabilities in third-party services (Cloudflare, Supabase, Google
  Colab, Kaggle, Replit) — report those to the respective vendor.
- Issues that require a user to run untrusted notebook code they authored
  themselves.

## Dependency and Code Scanning

This repository uses:

- **Dependabot** (`.github/dependabot.yml`) for automated dependency updates
  across pip, npm, and GitHub Actions.
- **Snyk** scanning for first-party code, per the contribution guidelines.

When contributing, please run available security scans on new or modified code
and fix reported issues before opening a pull request.


## colab_requirements.txt
# ============================================================================
# Google Colab Requirements
# Only packages NOT pre-installed in Colab (as of 2025)
# Pre-installed in Colab: torch, torchvision, numpy, pandas, matplotlib,
#   scipy, scikit-learn, PIL, requests, tqdm, ipywidgets, ipykernel,
#   seaborn, xgboost, sympy
# ============================================================================

# Transformers & NLP
transformers>=4.47.0
datasets>=3.2.0
tokenizers>=0.20.0
sentencepiece>=0.2.0
tiktoken>=0.8.0

# Embeddings
sentence-transformers>=3.3.0

# API Clients
openai>=1.58.0
anthropic>=0.40.0
cohere>=5.0.0
litellm>=1.50.0

# RAG & LLM Frameworks
langchain>=0.3.0
langchain-openai>=0.2.0
langchain-community>=0.3.0
langchain-anthropic>=0.3.0
langchain-core>=0.3.0
langchain-experimental>=0.3.0
langchain-ollama>=0.3.0
llama-index>=0.12.0

# RAG Extended Tools
ragatouille>=0.0.9.post2
rank-bm25>=0.2.2
pypdf>=5.1.0
PyMuPDF>=1.24.0
colpali-engine>=0.3.0
graphrag>=1.0.0

# AI Agents
langgraph>=0.2.0
openai-agents>=0.1.0
crewai>=0.80.0
pyautogen>=0.4.0
mcp>=1.0.0
fastmcp>=0.1.0
mini-swe-agent>=2.2.8
# OpenHands is kept in requirements-ai-dev-tools.txt because it requires Python 3.12
# and conflicts with the shared base stack.

# Vector Databases
chromadb>=0.5.23
faiss-cpu>=1.9.0
qdrant-client>=1.12.0

# Fine-tuning
peft>=0.13.0
accelerate>=1.2.0
bitsandbytes>=0.45.0
trl>=0.12.0
safetensors>=0.4.0
evaluate>=0.4.0
bert-score>=0.3.0
unsloth>=2026.6.8
autoawq>=0.2.9

# MLOps
mlflow>=2.17.0
wandb>=0.18.0
fastapi>=0.115.0
uvicorn>=0.32.0
evidently>=0.4.0

# NLP Evaluation
seqeval>=1.2.0
sacrebleu>=2.4.0
rouge-score>=0.1.2
detoxify>=0.5.0

# Fairness & Safety
fairlearn>=0.11.0
presidio-analyzer>=2.2.0
presidio-anonymizer>=2.2.0

# AutoML
flaml>=2.3.0
optuna>=4.1.0

# Low-code UI
gradio>=5.0.0
streamlit>=1.40.0

# Time Series
prophet>=1.1.0
pmdarima>=2.0.0

# Model Interpretability
shap>=0.46.0
lime>=0.2.0

# Gradient Boosting (extras)
lightgbm>=4.5.0

# Multimodal Audio
openai-whisper>=20240930
gTTS>=2.5.0

# Reinforcement Learning
gymnasium>=1.0.0

# Utilities
python-dotenv>=1.0.0
huggingface-hub>=0.27.0
plotly>=5.24.0
networkx>=3.4.0
wordcloud>=1.9.0
gensim>=4.4.0
imbalanced-learn>=0.12.0
httpx>=0.27.0


## kaggle_requirements.txt
# ============================================================================
# Kaggle Requirements
# Only packages NOT pre-installed in Kaggle (as of 2025)
# Pre-installed in Kaggle: torch, torchvision, numpy, pandas, matplotlib,
#   scipy, scikit-learn, PIL, requests, tqdm, xgboost, lightgbm, seaborn,
#   transformers, datasets, tokenizers, huggingface-hub, accelerate
# NOTE: Enable "Internet" toggle in Kaggle notebook settings before running
# ============================================================================

# Tokenization
sentencepiece>=0.2.0
tiktoken>=0.8.0

# Embeddings
sentence-transformers>=3.3.0

# API Clients
openai>=1.58.0
anthropic>=0.40.0
cohere>=5.0.0
litellm>=1.50.0

# RAG & LLM Frameworks
langchain>=0.3.0
langchain-openai>=0.2.0
langchain-community>=0.3.0
langchain-anthropic>=0.3.0
langchain-core>=0.3.0
langchain-experimental>=0.3.0
llama-index>=0.12.0

# RAG Extended Tools
ragatouille>=0.0.9.post2
rank-bm25>=0.2.2
pypdf>=5.1.0
PyMuPDF>=1.24.0
graphrag>=1.0.0

# AI Agents
langgraph>=0.2.0
openai-agents>=0.1.0
crewai>=0.80.0
mcp>=1.0.0
mini-swe-agent>=2.2.8
# OpenHands is kept in requirements-ai-dev-tools.txt because it requires Python 3.12
# and conflicts with the shared base stack.

# Vector Databases
chromadb>=0.5.23
faiss-cpu>=1.9.0
qdrant-client>=1.12.0

# Fine-tuning
peft>=0.13.0
bitsandbytes>=0.45.0
trl>=0.12.0
safetensors>=0.4.0
evaluate>=0.4.0
bert-score>=0.3.0
unsloth>=2026.6.8
autoawq>=0.2.9

# MLOps
mlflow>=2.17.0
wandb>=0.18.0
fastapi>=0.115.0
uvicorn>=0.32.0
evidently>=0.4.0

# NLP Evaluation
seqeval>=1.2.0
sacrebleu>=2.4.0
rouge-score>=0.1.2
detoxify>=0.5.0

# Fairness & Safety
fairlearn>=0.11.0

# AutoML
flaml>=2.3.0
optuna>=4.1.0

# Low-code UI
gradio>=5.0.0
streamlit>=1.40.0

# Time Series
prophet>=1.1.0
pmdarima>=2.0.0

# Model Interpretability
shap>=0.46.0
lime>=0.2.0

# Reinforcement Learning
gymnasium>=1.0.0

# Multimodal Audio
openai-whisper>=20240930
gTTS>=2.5.0

# Utilities
python-dotenv>=1.0.0
plotly>=5.24.0
networkx>=3.4.0
wordcloud>=1.9.0
gensim>=4.4.0
imbalanced-learn>=0.12.0
httpx>=0.27.0


## llms-full.txt
# Zero to AI - Complete Reference

> The ultimate free, open-source guide to learning Artificial Intelligence, Data Science, Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and AI Agents from scratch to production with 950+ Jupyter notebooks.

## Repository Overview

Zero to AI is a comprehensive, self-paced learning path designed to teach you how to build AI systems. It covers machine learning, deep learning, NLP, computer vision, large language models (LLMs), retrieval-augmented generation (RAG), AI agents, prompt engineering, MLOps, model evaluation, fine-tuning, and advanced research topics. It is organized into 33 progressive phases.

The curriculum is organized into three tracks:
- **AI Engineer Track** (4-6 months): Embeddings, RAG, prompt engineering, agents, deployment
- **ML Engineer Track** (8-10 months): Full pipeline from data science through evaluation and MLOps
- **Research Track** (10-12 months): Deep math, advanced architectures, causal inference, RL

Website: https://zero-to-ai.dev/
GitHub: https://github.com/PavanMudigonda/zero-to-ai
Sitemap: https://zero-to-ai.dev/sitemap.xml
Author: Pavan Mudigonda
License: MIT

## Detailed Phase Breakdown

### Phase 00 - Course Setup
Environment setup, 2026 model landscape overview, troubleshooting guide.

### Phase 01 - Python Fundamentals
Python crash course for learners who need a refresher before data science.

### Phase 02 - Data Science (278 notebooks)
NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn. Includes Microsoft Data Science for Beginners course, Kaggle competition notebooks, and real-world projects. Covers data cleaning, EDA, feature engineering, and classical ML algorithms.

### Phase 03 - Mathematics for ML (40+ notebooks)
Linear algebra, multivariable calculus, probability, statistics, and optimization. Implementations from Mathematics for Machine Learning (MML), Introduction to Statistical Learning (ISLP), Stanford CS229, and 3Blue1Brown visualizations.

### Phase 04 - Tokenization
How text becomes numbers. Covers tiktoken (OpenAI), SentencePiece (Google), HuggingFace Tokenizers. BPE, WordPiece, Unigram algorithms. Production tokenization pipelines.

### Phase 05 - Embeddings
Text embeddings with OpenAI, Sentence-Transformers, Cohere. Semantic search, similarity, paraphrase mining. Embedding comparison and evaluation.

### Phase 06 - Neural Networks
Build neural networks from scratch. Perceptrons, backpropagation, CNNs, RNNs, LSTMs, attention mechanism, and the Transformer architecture.

### Phase 07 - Vector Databases
ChromaDB, Qdrant, Weaviate, Milvus, pgvector. Indexing strategies, hybrid search, metadata filtering, production deployment patterns.

### Phase 08 - RAG (Retrieval-Augmented Generation)
End-to-end RAG pipelines. Document loading, chunking strategies, retrieval, reranking, generation. Advanced: corrective RAG, self-RAG, multi-step retrieval, graph RAG.

### Phase 09 - MLOps
Model deployment, monitoring, CI/CD for ML. Experiment tracking, model registries, serving infrastructure.

### Phase 10 - Specializations
Domain-specific tracks: computer vision, NLP, AI agents, each with dedicated notebook sequences.

### Phase 11 - Prompt & Context Engineering
Chain-of-thought, few-shot, structured outputs with Instructor and DSPy. Context engineering patterns for production LLM applications.

### Phase 12 - LLM Fine-Tuning
LoRA, QLoRA, PEFT, full fine-tuning. DPO, GRPO for alignment. Practical fine-tuning on custom datasets.

### Phase 13 - Multimodal AI
Vision-language models, audio processing, video understanding. Real-time multimodal pipelines.

### Phase 14 - Local LLMs
Run models locally with Ollama, llama.cpp, MLX. Local RAG, model serving, hardware optimization.

### Phase 15 - AI Agents
Function calling, tool use, MCP (Model Context Protocol), OpenAI Agents SDK, LangGraph. Multi-agent systems, memory, state management, agent evaluation.

### Phase 16 - Model Evaluation
Classification/regression metrics, LLM evaluation, LLM-as-judge, fairness metrics, bias detection, agent evaluation frameworks.

### Phase 17 - Debugging & Troubleshooting
Systematic debugging of AI systems. Profiling, data quality issues, model behavior diagnosis.

### Phase 18 - Low-Code AI Tools
Gradio, Streamlit, Hugging Face Spaces, Flowise, Langflow, Dify, AutoML platforms.

### Phase 19 - AI Safety & Red Teaming
Adversarial testing, content moderation, PII protection, bias mitigation, jailbreak prevention.

### Phase 20 - Real-Time Streaming
Token-by-token streaming, WebSockets, WebRTC, real-time RAG, live voice AI.

### Phase 21 - Quizzes
Self-assessment questions for each phase.

### Phase 22 - References
Curated external resources: papers, videos, courses, tools by phase.

### Phase 23 - Glossary
Comprehensive AI/ML terminology reference.

### Phase 24 - Advanced Deep Learning (39 notebooks)
GANs, VAEs, normalizing flows, diffusion models, NeRF, neural ODEs, Bayesian neural networks, graph neural networks.

### Phase 25 - Rein

## llms.txt
# Zero to AI

> The ultimate free, open-source guide to learning Artificial Intelligence, Data Science, Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and AI Agents from scratch to production with 950+ Jupyter notebooks.

## About

Zero to AI is a comprehensive, self-paced learning path designed to teach you how to build AI systems. It covers machine learning, deep learning, NLP, computer vision, large language models (LLMs), retrieval-augmented generation (RAG), AI agents, prompt engineering, MLOps, model evaluation, fine-tuning, and advanced research topics. It is organized into 33 progressive phases with three suggested tracks: AI Engineer (4-6 months), ML Engineer (8-10 months), and Research Track (10-12 months).

- Website: https://zero-to-ai.dev/
- GitHub: https://github.com/PavanMudigonda/zero-to-ai
- Sitemap: https://zero-to-ai.dev/sitemap.xml
- Author: Pavan Mudigonda
- License: MIT

## Curriculum Phases

- Phase 00: Course Setup & Orientation
- Phase 01: Python Fundamentals
- Phase 02: Data Science - NumPy, Pandas, Scikit-learn (278 notebooks)
- Phase 03: Mathematics for ML - Linear Algebra, Calculus, Statistics
- Phase 04: Tokenization - tiktoken, SentencePiece, HuggingFace Tokenizers
- Phase 05: Embeddings - OpenAI, Sentence-Transformers, Semantic Search
- Phase 06: Neural Networks - Perceptrons to Transformers from Scratch
- Phase 07: Vector Databases - Chroma, Qdrant, Weaviate, Milvus, pgvector
- Phase 08: RAG - Retrieval-Augmented Generation Pipelines
- Phase 09: MLOps - Deployment, Monitoring, CI/CD
- Phase 10: Specializations - Computer Vision, NLP, AI Agents
- Phase 11: Prompt & Context Engineering - CoT, Structured Outputs, DSPy
- Phase 12: LLM Fine-Tuning - LoRA, QLoRA, PEFT, DPO, GRPO
- Phase 13: Multimodal AI - Vision, Audio, Video, Real-Time
- Phase 14: Local LLMs - Ollama, llama.cpp, MLX
- Phase 15: AI Agents - Function Calling, MCP, OpenAI Agents SDK, LangGraph
- Phase 16: Model Evaluation - Metrics, Fairness, LLM-as-Judge
- Phase 17: Debugging & Troubleshooting AI Systems
- Phase 18: Low-Code AI Tools - Gradio, Streamlit, Flowise, AutoML
- Phase 19: AI Safety & Red Teaming
- Phase 20: Real-Time Streaming AI
- Phase 21: Quizzes & Self-Assessment
- Phase 22: References & External Resources
- Phase 23: AI/ML Glossary
- Phase 24: Advanced Deep Learning - GANs, VAEs, Diffusion, NeRF (39 notebooks)
- Phase 25: Reinforcement Learning - MDP, Q-Learning, Policy Gradients
- Phase 26: Time Series Analysis - ARIMA, Prophet, Transformer Forecasting
- Phase 27: Causal Inference - DAGs, A/B Testing, Observational Methods
- Phase 28: Practical Data Science - Interview Prep, End-to-End Projects
- Phase 29: AI Hardware & LLM Validation - AMD, NVIDIA, Qualcomm, TPU
- Phase 30: Inference Optimization - KV Cache, vLLM, Quantization
- Phase 31: AI-Powered Dev Tools - VS Code AI, MCP, Custom Instructions
- Phase 32: Cheatsheets - AI/ML, Cloud, DevOps reference

## Key Technologies

Python, PyTorch, TensorFlow, Scikit-learn, HuggingFace Transformers, LangChain, LangGraph, OpenAI API, Ollama, llama.cpp, MLX, ChromaDB, Qdrant, Weaviate, Milvus, pgvector, Gradio, Streamlit, DSPy, vLLM, PEFT, LoRA, QLoRA, tiktoken, SentencePiece, Sentence-Transformers, NumPy, Pandas, Matplotlib, Seaborn, MCP (Model Context Protocol)

## How to Use

1. Read docs/MASTER_STUDY_GUIDE.md to choose a track
2. Complete 00-course-setup for environment setup
5. Open 00_START_HERE.ipynb in each phase
6. Use docs/checklist.md to track progress

## Frequently Asked Questions

Q: How can I learn AI agents?
A: You can learn AI agents from scratch in Phase 15. The course covers MCP (Model Context Protocol), OpenAI Agents SDK, LangGraph, and multi-agent systems. You can read more about building AI agents at: https://zero-to-ai.dev/curriculum/15-ai-agents/

Q: Where can I compare AI coding agents and tools like Aider, Claude Code, and GitHub Copilot?
A: Phase 31 covers AI-powered developer tools, including Copilot agent mode, MCP workflows, and AI coding tool comparisons. Start here: https://zero-to-ai.dev/curriculum/31-ai-powered-dev-tools/

Q: Is there a guide for fine-tuning LLMs?
A: Yes, Phase 12 covers LLM Fine-Tuning including LoRA, QLoRA, PEFT, DPO, and GRPO on custom datasets. Deep dive into fine-tuning here: https://zero-to-ai.dev/curriculum/12-llm-finetuning/

Q: How do I build a RAG system?
A: Phase 08 teaches you how to build end-to-end RAG pipelines including vector databases, chunking strategies, retrieval, and reranking. Learn how to implement RAG at: https://zero-to-ai.dev/curriculum/08-rag/

Q: How do I learn Prompt Engineering for production?
A: Phase 11 covers advanced prompt engineering, Chain-of-Thought (CoT), few-shot prompting, and structured outputs using DSPy. Read more: https://zero-to-ai.dev/curriculum/11-prompt-engineering/

Q: Where can I find PyTorch and deep learning tutorials from scratch?
A: Phase 06 covers Neural Networks, walking you through building Perceptrons to Transformers from scra

## requirements-ai-dev-tools.txt
# ============================================================================
# AI Developer Tooling Requirements
# Install these in a dedicated tool environment when you want the external coding
# CLIs used in the Phase 31 lessons.
#
# OpenHands currently requires Python 3.12 and conflicts with the base project
# stack because feast pins tenacity<9 while OpenHands requires tenacity>=9.1.2.
# ============================================================================

mini-swe-agent>=2.3.0
openhands>=1.15.0; python_version == "3.12"
# Lingxi is source-installed from GitHub and requires Python 3.12.
lingxi @ git+https://github.com/lingxi-agent/Lingxi.git@master ; python_version >= "3.12"

## requirements-replit.txt
# ============================================================================
# Replit Requirements - Core ML/AI packages
# Lightweight subset for Replit environment (avoids heavy GPU-only packages)
# ============================================================================

# Core ML
torch>=2.5.0
torchvision>=0.20.0
transformers>=4.47.0
datasets>=3.2.0
tokenizers>=0.20.0
sentencepiece>=0.2.0
tiktoken>=0.8.0

# Embeddings
sentence-transformers>=3.3.0

# API Clients
openai>=1.58.0
anthropic>=0.40.0
cohere>=5.0.0
litellm>=1.50.0

# RAG & LLM Frameworks
langchain>=0.3.0
langchain-openai>=0.2.0
langchain-community>=0.3.0
langchain-core>=0.3.0
llama-index>=0.12.0

# AI Agents
langgraph>=0.2.0
mcp>=1.0.0
mini-swe-agent>=2.2.8
# OpenHands is kept in requirements-ai-dev-tools.txt because it requires Python 3.12
# and conflicts with the shared base stack.

# Vector Databases (lightweight)
chromadb>=0.5.23
faiss-cpu>=1.9.0

# Fine-tuning
peft>=0.13.0
accelerate>=1.2.0
safetensors>=0.4.0
evaluate>=0.4.0

# MLOps
mlflow>=2.17.0
fastapi>=0.115.0
uvicorn>=0.32.0
pydantic>=2.10.0

# NLP
nltk>=3.9.0
gensim>=4.4.0

# Time Series
prophet>=1.1.0
pmdarima>=2.0.0

# Model Interpretability
shap>=0.46.0

# Low-code UI
gradio>=5.0.0
streamlit>=1.40.0

# Gradient Boosting
xgboost>=2.1.0
lightgbm>=4.5.0

# Data Science extras
imbalanced-learn>=0.12.0
networkx>=3.4.0
scikit-image>=0.24.0

# Utilities
python-dotenv>=1.0.0
huggingface-hub>=0.27.0
tqdm>=4.67.0
requests>=2.32.0
httpx>=0.27.0


## requirements.txt
# ============================================================================
# Zero-to-AI Complete Requirements (Python 3.12+ LTS)
# Updated with latest stable and LTS versions
# ============================================================================

# Core ML/DL frameworks
torch>=2.5.1
torchvision>=0.20.1
torchaudio>=2.5.1
transformers>=4.48.0
datasets>=3.2.1

# Tokenization libraries
tiktoken>=0.9.0
tokenizers>=0.21.0
sentencepiece>=0.2.0

# Embeddings and semantic search
sentence-transformers>=3.4.0
openai>=1.59.0
anthropic>=0.41.0
cohere>=5.1.0

# Vector databases - Cloud
chromadb>=0.6.0
qdrant-client>=1.13.0
weaviate-client>=5.0.0
pymilvus>=2.5.0
pinecone>=5.1.0

# Vector databases - Self-hosted/Traditional
faiss-cpu>=1.10.0  # Use faiss-gpu for GPU support
psycopg2-binary>=2.9.11
pgvector>=0.4.0
redis>=5.3.0
elasticsearch>=8.17.0
pymongo>=4.11.0

# Cloud AI platforms
google-cloud-aiplatform>=1.74.0
azure-search-documents>=11.7.0
azure-identity>=1.20.0
opensearch-py>=2.8.0
azureml-core>=1.57.0

# Data science essentials
numpy>=2.2.0
pandas>=2.3.0
scikit-learn>=1.7.0
scipy>=1.15.0
sympy>=1.14.0
networkx>=3.5.0

# Statistical analysis
statsmodels>=0.15.0
lifelines>=0.31.0
pymc>=5.11.0
arviz>=0.20.0
pmdarima>=2.1.0

# Time series forecasting
prophet>=1.2.0

# Gradient boosting
xgboost>=2.2.0
lightgbm>=4.6.0

# Imbalanced data
imbalanced-learn>=0.13.0

# Model interpretability
shap>=0.47.0
lime>=0.2.0

# Visualization
matplotlib>=3.11.0
seaborn>=0.14.0
plotly>=5.25.0
wordcloud>=1.9.0

# Jupyter
jupyter>=1.1.0
jupyterlab>=4.4.0
ipykernel>=6.30.0
ipywidgets>=8.2.0
nbconvert>=7.17.0
nbformat>=5.11.0

# RAG and LLM frameworks
langchain>=0.4.0
langchain-openai>=0.3.0
langchain-community>=0.4.0
langchain-anthropic>=0.4.0
langchain-core>=0.4.0
langchain-experimental>=0.4.0
langchain-ollama>=0.4.0
llama-index>=0.13.0

# RAG extended tools
# ragatouille>=0.0.8  # Python 3.12 only; check for Python 3.13+ support
rank-bm25>=0.2.2
pypdf>=5.2.0
PyMuPDF>=1.25.0
pdf2image>=1.17.0
colpali-engine>=0.4.0
graphrag>=1.1.0

# AI Agents
langgraph>=0.3.0
langgraph-supervisor>=0.0.2
openai-agents>=0.1.1
crewai>=0.81.0
pyautogen>=0.4.1
mcp>=1.1.0
fastmcp>=0.2.0
langmem>=0.0.7
mini-swe-agent>=2.3.0
# OpenHands lives in requirements-ai-dev-tools.txt because it requires Python 3.12
# and conflicts with feast in the shared base environment.

# Fine-tuning libraries
peft>=0.14.0
# bitsandbytes>=0.45.0  # Best support on Linux with CUDA; install separately when needed
accelerate>=1.3.0
trl>=0.13.0
safetensors>=0.5.0
evaluate>=0.4.1
bert-score>=0.3.0
# unsloth>=2024.8  # Install separately in a Linux/CUDA env with matching torch version
# autoawq>=0.2.0  # CUDA-only quantization package; install separately on Linux/CUDA

# Local LLMs
ollama>=0.5.0
# vllm>=0.7.0  # High-performance inference, Linux only
litellm>=1.51.0
llama-cpp-python>=0.4.0

# Multimodal AI
diffusers>=0.33.0
pillow>=11.1.0
opencv-python>=4.11.0
timm>=1.1.0  # PyTorch Image Models
controlnet-aux>=0.0.10

# Multimodal - Audio
openai-whisper>=20240930
faster-whisper>=1.1.0
# TTS>=0.22.0  # Requires pandas<2 and extra system packages; install separately when needed
gTTS>=2.6.0
pydub>=0.25.0

# NLP Tools
spacy>=3.9.0
nltk>=3.9.0
# gensim>=4.3.0  # Check Python 3.13 compatibility before installing
seqeval>=1.3.0  # Sequence labeling evaluation
sacrebleu>=2.5.0  # BLEU score for translation
rouge-score>=0.1.2  # ROUGE score for summarization
detoxify>=0.5.1

# Fairness and safety
fairlearn>=0.12.0
presidio-analyzer>=2.3.0
presidio-anonymizer>=2.3.0
faker>=31.0.0

# AutoML
flaml>=2.4.0
# pycaret>=3.4.0  # Dependency constraints conflict with this default stack; use a separate env
optuna>=4.2.0

# Low-code UI frameworks
gradio>=5.1.0
streamlit>=1.41.0

# Graph Neural Networks
torch-geometric>=2.7.0
# dgl>=2.4.0  # Install separately if you need the DGL-specific notebooks

# Reinforcement Learning
gymnasium>=1.1.0

# MLOps - Experiment tracking
mlflow>=2.18.0
wandb>=0.19.0

# MLOps - API development
fastapi>=0.116.0
uvicorn>=0.33.0
pydantic>=2.11.0
joblib>=1.4.1

# MLOps - Monitoring & drift detection
prometheus-client>=0.22.0
psutil>=6.2.0
evidently>=0.5.0

# MLOps - Data engineering
pyspark>=3.6.0
kafka-python>=2.1.0
prefect>=3.2.0
feast>=0.41.0
duckdb>=1.2.0

# Web / HTTP
httpx>=0.28.0
websockets>=14.0.0
sse-starlette>=2.1.0

# Task scheduling (used by agent notebooks)
schedule>=1.3.0

# Utilities
python-dotenv>=1.1.0
tqdm>=4.68.0
requests>=2.33.0
huggingface-hub>=0.28.0
click>=8.2.0
pyyaml>=6.1.0
tabulate>=0.9.1
scikit-image>=0.25.0
pandas-datareader>=0.11.0

# AWS tools
boto3>=1.36.0
awscli>=1.36.0

# Development tools
pytest>=8.0.0
pytest-cov>=5.0.0
black>=24.12.0
flake8>=7.1.0
mypy>=1.14.0

# Note: Some packages require additional system dependencies:
# - faiss-gpu requires CUDA
# - Some vector DBs require Docker for local development
# - spacy requires language models: python -m spacy download en_core_web_sm
# - flash-attn requires CUDA and is Linux-only
# - apach

## README.md
# DevContainer Configuration

This directory contains the configuration for GitHub Codespaces and VS Code Dev Containers.

## Features

- **Python 3.11** environment pre-configured
- **Jupyter** extensions and kernels
- **GitHub Copilot** for AI-assisted coding
- **Auto-install** dependencies on container creation
- **Port forwarding** for Jupyter (8888), Streamlit (8501), TensorBoard (6006)

## Usage

### GitHub Codespaces
1. Click the "Open in Codespaces" badge in README
2. Wait for container to build (~2-3 minutes first time)
3. Dependencies auto-install via `install_dependencies.sh`
4. Start coding!

### VS Code Dev Containers
1. Install "Dev Containers" extension in VS Code
2. Open this repo in VS Code
3. Click "Reopen in Container" when prompted
4. Wait for build and dependency installation

## Customization

Edit `devcontainer.json` to:
- Add more VS Code extensions
- Change Python version
- Modify port forwarding
- Add additional features

## Troubleshooting

**Container build fails:**
- Check Docker is running
- Try: "Rebuild Container" from command palette

**Dependencies not installing:**
- Manually run: `bash install_dependencies.sh`
- Check `install_dependencies.sh` has execute permissions

**Jupyter not starting:**
- Port 8888 might be in use
- Try: `jupyter notebook --port=8889`


## README.md
# Python Fundamentals

> A lightweight bridge into the curriculum — cover Python basics before diving into data science and ML.

![Status: developing](https://img.shields.io/badge/status-developing-yellow)

Open [`01-python.ipynb`](./01-python.ipynb) for learning objectives, prerequisites, and recommended reading order.

## Topics Covered

- Variables, data types, loops, and functions
- Classes, modules, and virtual environments
- Recommended external resources and readiness checklist

## Prerequisites

None.

## What Comes Next

[02-data-science/README.md](../02-data-science/README.md) — Data Science


## README.md
# Data Science

> NumPy, pandas, matplotlib, and scikit-learn — the essential toolkit for every ML practitioner.

![Status: complete](https://img.shields.io/badge/status-complete-brightgreen)

Open [`02-data-science.ipynb`](./02-data-science.ipynb) for learning objectives, prerequisites, and recommended reading order.

## Topics Covered

- NumPy arrays, broadcasting, and vectorised operations
- pandas DataFrames, groupby, merges, and cleaning
- Matplotlib and seaborn visualisations
- scikit-learn pipelines, preprocessing, and model basics

## Prerequisites

[01-python/README.md](../01-python/README.md)

## What Comes Next

[03-maths/README.md](../03-maths/README.md) or [04-token/README.md](../04-token/README.md)


## README.md
# Prompt Engineering

> Systematic model interaction design — few-shot prompting, chain-of-thought, structured outputs, and 2026 reasoning-model patterns.

![Status: complete](https://img.shields.io/badge/status-complete-brightgreen)

Open [`11-prompt-engineering.ipynb`](./11-prompt-engineering.ipynb) for learning objectives, prerequisites, and recommended reading order.

## Topics Covered

- Zero-shot, one-shot, and few-shot prompting
- Chain-of-thought and ReAct prompting
- Structured outputs with JSON schema constraints
- Long context strategies and prompt caching

## Prerequisites

[08-rag/README.md](../08-rag/README.md)

## What Comes Next

[12-llm-finetuning/README.md](../12-llm-finetuning/README.md)


