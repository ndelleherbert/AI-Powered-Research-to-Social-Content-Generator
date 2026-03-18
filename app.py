import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
import os

st.set_page_config(
    page_title="AI-Powered Research-to-Social Content Generator ",
    page_icon="🚀",
    layout="wide",
)

# ── API Key ───────────────────────────────────────────────────────────────────

def get_api_key() -> str | None:
    try:
        if "ANTHROPIC_API_KEY" in st.secrets:
            return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        pass
    return os.environ.get("ANTHROPIC_API_KEY")


# ── Chain Builder ─────────────────────────────────────────────────────────────

def build_chains(api_key: str):
    llm = ChatAnthropic(
        model="claude-sonnet-4-5",
        api_key=api_key,
        temperature=0.7,
        max_tokens=1024,
    )
    parser = StrOutputParser()

    # Chain 1 — Research Report
    research_prompt = PromptTemplate(
        input_variables=["user_input"],
        template=(
            "You are an expert researcher and writer.\n"
            "Topic: {user_input}\n\n"
            "Generate a comprehensive, well-structured research report with:\n"
            "- Executive Summary\n"
            "- Background & History\n"
            "- Current State\n"
            "- Major Trends\n"
            "- Challenges & Opportunities\n"
            "- Conclusion\n\n"
            "Use clear headings. Write 400-600 words in a professional tone."
        ),
    )
    research_chain = research_prompt | llm | parser

    # Chain 2 — 5-Bullet Summary
    summary_prompt = PromptTemplate(
        input_variables=["research"],
        template=(
            "You are a professional content summarizer.\n"
            "Based on the research report below, produce exactly 5 concise bullet points "
            "capturing the most important insights. Each bullet must be one sentence "
            "starting with a strong verb.\n\n"
            "Research:\n{research}"
        ),
    )
    summary_chain = summary_prompt | llm | parser

    # Chain 3a — LinkedIn
    linkedin_prompt = PromptTemplate(
        input_variables=["summary"],
        template=(
            "You are a LinkedIn content strategist.\n"
            "Write a LinkedIn post from the summary below.\n\n"
            "STRICT CONSTRAINTS:\n"
            "- 120-180 words exactly\n"
            "- First 2 lines: powerful hook (no fluff)\n"
            "- Short lines (max 12 words per line)\n"
            "- Include exactly 1 actionable tip\n"
            "- End with exactly 1 thought-provoking question\n"
            "- 3-6 hashtags on the last line\n"
            "- Tone: confident, helpful, professional\n\n"
            "Summary:\n{summary}"
        ),
    )

    # Chain 3b — Facebook
    facebook_prompt = PromptTemplate(
        input_variables=["summary"],
        template=(
            "You are a Facebook content creator.\n"
            "Write an engaging Facebook post from the summary below.\n\n"
            "Guidelines:\n"
            "- 80-150 words\n"
            "- Conversational, warm, community tone\n"
            "- Start with a relatable hook or question\n"
            "- Include a clear call-to-action\n"
            "- 2-4 emojis woven in naturally\n"
            "- End with 2-4 hashtags\n\n"
            "Summary:\n{summary}"
        ),
    )

    # Chain 3c — Instagram
    instagram_prompt = PromptTemplate(
        input_variables=["summary"],
        template=(
            "You are an Instagram content creator.\n"
            "Write a punchy Instagram caption from the summary below.\n\n"
            "Guidelines:\n"
            "- 60-120 words\n"
            "- First line: bold, scroll-stopping statement\n"
            "- Use line breaks for readability\n"
            "- 3-5 expressive emojis\n"
            "- 5-10 hashtags at the end (mix popular + niche)\n\n"
            "Summary:\n{summary}"
        ),
    )

    parallel_social = RunnableParallel(
        linkedin=linkedin_prompt   | llm | parser,
        facebook=facebook_prompt   | llm | parser,
        instagram=instagram_prompt | llm | parser,
    )

    return research_chain, summary_chain, parallel_social


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("⚙️ Configuration")
    st.divider()
    st.markdown("### 🔄 Pipeline")
    st.markdown("""
1. 📝 **Topic Input**
2. 📄 **Research Report** — Chain 1
3. 🔍 **5-Bullet Summary** — Chain 2
4. 📣 **Social Posts ×3** — RunnableParallel
   - 🔗 LinkedIn
   - 📘 Facebook
   - 📸 Instagram
""")
    st.divider()
    st.caption("Model: `claude-sonnet-4-5`  \nBuilt with LangChain + Streamlit")


# ── Main ──────────────────────────────────────────────────────────────────────

st.title("🚀 AI-Powered Research-to-Social Content Generator ")
st.caption("Topic → Research Report → Summary → LinkedIn · Facebook · Instagram")
st.divider()

# Step 1 — Topic input
st.subheader("Step 1 — Enter a Topic")
topic = st.text_input(
    "Topic",
    placeholder="e.g. Indian Premier League, Quantum Computing, Remote Work Trends…",
    label_visibility="collapsed",
)
generate = st.button("✦ Generate Content", type="primary")


# ── Pipeline Execution ────────────────────────────────────────────────────────

if generate:
    if not topic.strip():
        st.warning("⚠️ Please enter a topic before generating.")
        st.stop()

    api_key = get_api_key()
    if not api_key:
        st.error(
            "🔑 Anthropic API key not found. "
            "Add it in the sidebar, set `ANTHROPIC_API_KEY` as an env variable, "
            "or add it to `.streamlit/secrets.toml`."
        )
        st.stop()

    try:
        research_chain, summary_chain, parallel_social = build_chains(api_key)
    except Exception as e:
        st.error(f"Failed to initialise chains: {e}")
        st.stop()

    st.divider()

    # ── Stage 1 : Research ────────────────────────────────────────────────────
    st.subheader("📄 Step 2 — Research Report")
    with st.spinner("Generating research report…"):
        try:
            research_result = research_chain.invoke({"user_input": topic})
        except Exception as e:
            st.error(f"Research generation failed: {e}")
            st.stop()

    with st.expander("View Full Research Report", expanded=True):
        st.markdown(research_result)

    st.success("✅ Research report generated!")
    st.divider()

    # ── Stage 2 : Summary ─────────────────────────────────────────────────────
    st.subheader("🔍 Step 3 — 5-Bullet Summary")
    with st.spinner("Summarising into 5 key bullet points…"):
        try:
            summary_result = summary_chain.invoke({"research": research_result})
        except Exception as e:
            st.error(f"Summary generation failed: {e}")
            st.stop()

    st.markdown(summary_result)
    st.success("✅ Summary complete!")
    st.divider()

    # ── Stage 3 : Parallel Social Posts ──────────────────────────────────────
    st.subheader("📣 Step 4 — Social Media Posts")
    st.caption("All 3 posts generated simultaneously via `RunnableParallel`")

    with st.spinner("Generating LinkedIn, Facebook & Instagram posts in parallel…"):
        try:
            social_results = parallel_social.invoke({"summary": summary_result})
        except Exception as e:
            st.error(f"Social post generation failed: {e}")
            st.stop()

    col_li, col_fb, col_ig = st.columns(3)

    with col_li:
        st.markdown("#### 🔗 LinkedIn")
        st.text_area(
            label="LinkedIn Post",
            value=social_results["linkedin"],
            height=320,
            label_visibility="collapsed",
            key="li_out",
        )

    with col_fb:
        st.markdown("#### 📘 Facebook")
        st.text_area(
            label="Facebook Post",
            value=social_results["facebook"],
            height=320,
            label_visibility="collapsed",
            key="fb_out",
        )

    with col_ig:
        st.markdown("#### 📸 Instagram")
        st.text_area(
            label="Instagram Post",
            value=social_results["instagram"],
            height=320,
            label_visibility="collapsed",
            key="ig_out",
        )

    st.success("🎉 All content generated! Copy any post from the boxes above.")
    st.divider()

    # Debug expander
    with st.expander("🗂 Raw pipeline output (debug)"):
        st.json({
            "topic": topic,
            "research_chars": len(research_result),
            "summary": summary_result,
            "linkedin": social_results["linkedin"],
            "facebook": social_results["facebook"],
            "instagram": social_results["instagram"],
        })

else:
    st.info("👆 Enter a topic above and click **Generate Content** to run the full pipeline.")
