

import streamlit as st
import pymupdf
import re

# --------------------------------
# APPLICATION TITLE
# --------------------------------

st.set_page_config(
    page_title="Chat with PDF",
    page_icon="📄"
)

st.title("📄 Chat with PDF")
st.write("Upload a PDF and ask questions about it.")


# --------------------------------
# PDF UPLOAD
# --------------------------------

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)


# --------------------------------
# STOP WORDS
# --------------------------------

stop_words = {
    "what", "is", "are", "was", "were",
    "the", "a", "an", "of", "in", "on",
    "to", "for", "and", "or", "how",
    "why", "when", "where", "which",
    "who", "explain", "describe", "tell",
    "me", "about", "does", "do", "can",
    "could", "would", "should", "please",
    "give", "define", "meaning", "this",
    "that", "it", "its", "with", "from"
}


# --------------------------------
# EXTRACT PDF TEXT
# --------------------------------

if uploaded_file is not None:

    try:

        pdf = pymupdf.open(
            stream=uploaded_file.getvalue(),
            filetype="pdf"
        )

        pdf_pages = []

        for page_number, page in enumerate(pdf):

            text = page.get_text()

            pdf_pages.append({
                "page": page_number + 1,
                "text": text
            })

        pdf.close()

        if not any(page["text"].strip() for page in pdf_pages):
            st.warning(
                "No readable text found. "
                "This may be a scanned PDF."
            )

        else:

            st.success("PDF uploaded successfully!")

            st.write(
                f"Total pages: {len(pdf_pages)}"
            )

            # --------------------------------
            # QUESTION INPUT
            # --------------------------------

            question = st.text_input(
                "Ask a question about your PDF:"
            )

            if st.button("Get Answer"):

                if not question.strip():

                    st.warning("Please enter a question.")

                else:

                    # --------------------------------
                    # PROCESS QUESTION
                    # --------------------------------

                    words = set(re.findall(
                        r"\b[a-zA-Z0-9]+\b",
                        question.lower()
                    )) - stop_words

                    results = []

                    # --------------------------------
                    # SEARCH PDF CONTENT
                    # --------------------------------

                    for page in pdf_pages:

                        sentences = re.split(
                            r"(?<=[.!?])\s+",
                            page["text"]
                        )

                        for sentence in sentences:

                            sentence_words = set(re.findall(
                                r"\b[a-zA-Z0-9]+\b",
                                sentence.lower()
                            )) - stop_words

                            if not sentence_words:
                                continue

                            matched_words = words & sentence_words

                            # Calculate relevance score
                            score = (
                                len(matched_words) / len(words)
                                if words else 0
                            )

                            if len(matched_words) >= 1:

                                results.append((
                                    score,
                                    page["page"],
                                    sentence.strip()
                                ))

                    # --------------------------------
                    # DISPLAY RESULTS
                    # --------------------------------

                    results.sort(
                        key=lambda x: x[0],
                        reverse=True
                    )

                    if results:

                        st.subheader(
                            "📖 Relevant Information"
                        )

                        for score, page, sentence in results[:5]:

                            st.write(sentence)

                            st.caption(
                                f"Source: Page {page}"
                            )

                    else:

                        st.warning(
                            "Sorry, I couldn't find relevant "
                            "information about your question "
                            "in the uploaded PDF."
                        )

    except Exception as e:

        st.error(f"Error reading PDF: {e}")
