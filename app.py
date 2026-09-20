from langchain_groq import ChatGroq
import validators, streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader, WebBaseLoader
import os

## Streamlit app

st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜🔗")
st.title("🦜🔗 LangChain: Summarize Text From YT or Website")
st.subheader("Summarize URL")

## Get the Groq API Key and URL (YT or Website) to be Summarized

with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")
    st.markdown("---")
    st.markdown("Developed by [Adarsh Yadav](https://dev-adarshy.in)")

generic_url = st.text_input("URL", label_visibility="collapsed")

## Prompt template
promot_template = """
You are a thoughtful person who has just finished reading or watching the content below, and now you're explaining it to a friend.

Write a summary of about 300 words:
- Write in the same language as the content.
- Use a natural, conversational tone, like a person talking, not a report.
- Write in flowing paragraphs. No bullet points, headings, or lists.
- Start with what the content is really about, then cover the key ideas in the order that makes the most sense, then end with the main takeaway.
- Include important facts, numbers, or names only when they matter.
- Never use phrases like "the text says", "the transcript states", or "this content discusses". Just explain the ideas directly.
- Don't add opinions or details that aren't in the content.

Content:
{text}
"""
promot = PromptTemplate(template=promot_template, input_variables=["text"])

## Validate all the inputs
if st.button("Summarize the Content from YT or Website"):
    ## Validate all the inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL. It can be a YT video URL or Website URL")
    else:
        try:
            with st.spinner("Waiting....."):
                ## LLM (created after the key is validated, so the app doesn't crash on load)
                llm = ChatGroq(model="openai/gpt-oss-20b", groq_api_key=groq_api_key)

                ## loading the website or Yt video data
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=False,language=["en", "hi"])
                else:
                    loader = WebBaseLoader(
                        generic_url,
                        header_template={"User-Agent": "Mozilla/5.0"},
                    )
                docs = loader.load()

                text = "\n\n".join(d.page_content for d in docs).strip()

                if len(text) < 300:
                    st.error(
                        "Couldn't extract readable content from this page. "
                        "It is likely paywalled, blocking scrapers, or rendered with JavaScript."
                    )
                    st.stop()

                text = text[:12000]  # keep within token limits

                ## Chain For Summarization
                Chain = promot | llm | StrOutputParser()
                output_summary = Chain.invoke({"text": text})

                st.success(output_summary)
        except Exception as e:
            st.error(f"An error occurred: {e}")