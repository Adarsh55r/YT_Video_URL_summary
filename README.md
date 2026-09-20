# YT & Website Summarizer

Paste a YouTube link or a blog URL, and get a short summary that reads like a person wrote it.

I built this because I was tired of opening a 40-minute video or a long article just to find out it wasn't worth my time. Now I paste the link, read 300 words, and decide.

It runs on Streamlit, uses LangChain to glue things together, and Groq to do the actual summarizing (fast, and the free tier is enough for personal use).

## What it does

- Summarizes YouTube videos from their transcript
- Summarizes regular web pages and blog posts
- Writes the summary in the **same language as the content**, so a Hindi video gets a Hindi summary
- Keeps the tone natural and conversational instead of a stiff bullet-point report
- Uses `openai/gpt-oss-20b` on Groq, and switching to another model is a one-line change in the code

## Setup

You'll need Python 3.10+ and a free API key from [Groq](https://console.groq.com).

```bash
# clone the repo and go into the folder
git clone <your-repo-url>
cd <your-repo-folder>

# create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# install dependencies
pip install streamlit langchain-groq langchain-core langchain-community validators youtube-transcript-api pytube beautifulsoup4 unstructured
```

## Run it

```bash
streamlit run app.py
```

Then in the browser:

1. Paste your Groq API key in the sidebar
2. Paste a YouTube or website URL
3. Click **Summarize**

## Things worth knowing

**Groq models change often.** The app uses `openai/gpt-oss-20b`, set in this line of `app.py`:

```python
llm = ChatGroq(model="openai/gpt-oss-20b", groq_api_key=groq_api_key)
```

If you get a `model_not_found` error, the model was probably retired or your account can't access it. Grab a current model name from the Groq console, replace it in that line, and restart the app.

**Some websites won't work.** Paywalled sites (the Economist, NYT, WSJ), login-only pages, and sites that render everything with JavaScript block simple scrapers. The app will tell you it couldn't read the page instead of making something up.

**YouTube needs a transcript.** If a video has no captions at all, there's nothing to summarize. By default the app looks for English and Hindi transcripts. To support more languages, add their codes to the `language` list in the `YoutubeLoader` line, for example `["en", "hi", "es", "fr"]`.

**Long content gets trimmed.** To stay within token limits, only the first 12,000 characters are sent to the model. For very long videos or articles, the summary covers the early part. You can raise this limit if your plan allows it. Non-Latin scripts like Hindi use more tokens per character, so lower it if you hit limit errors.

## Tech stack

- [Streamlit](https://streamlit.io) for the UI
- [LangChain](https://www.langchain.com) for the prompt and chain
- [Groq](https://groq.com) for the LLM
- `youtube-transcript-api` for YouTube transcripts
- `WebBaseLoader` + BeautifulSoup for web pages

## Customizing the summary style

The summary style lives in `promot_template` in `app.py`. Want it more formal, shorter, or in bullet points? Edit that prompt. It's plain English, so no code changes are needed.

## Developed by

**Adarsh Yadav**
Portfolio: [dev-adarshy.in](https://dev-adarshy.in)
GitHub : (https://github.com/Adarsh55r)

If you find a bug or have an idea to make it better, feel free to open an issue or reach out through my portfolio.
