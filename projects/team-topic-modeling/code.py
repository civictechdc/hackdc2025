#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 12:15:12 2025

@author: anaswarjayakumar
"""

# %%
import spacy
import re
from rake_nltk import Rake
from collections import defaultdict
# %%
# import sys
# print("Python executable:", sys.executable)
# %%
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("The Postal Regulatory Commission regulates USPS and ensures transparency.")
for ent in doc.ents:
    print(ent.text, ent.label_)

# %%
import nltk
nltk.download('stopwords')
# %%
# %%

import spacy
import re
from rake_nltk import Rake
from collections import defaultdict
import pandas as pd
import seaborn as sns
from IPython import get_ipython
from nltk.corpus import stopwords

def extract_regulatory_sentences(text):
    # Define common regulatory keywords
    regulation_keywords = [
        "shall", "must", "prohibited", "not allowed", "required",
        "may not", "forbidden", "is illegal", "mandated"
    ]
    sentences = re.split(r'(?<=[.!?])\s+', text)
    regulatory_sentences = [
        sentence for sentence in sentences
        if any(keyword in sentence.lower() for keyword in regulation_keywords)
    ]
    return regulatory_sentences

def extract_topics_and_keywords(sentences, nlp):
    topic_keywords = defaultdict(list)
    rake = Rake(language='english')
    
    for sentence in sentences:
        doc = nlp(sentence)
        topics = set(chunk.text.lower() for chunk in doc.noun_chunks)
        rake.extract_keywords_from_text(sentence)
        keywords = rake.get_ranked_phrases()
        for topic in topics:
            topic_keywords[topic].extend(keywords)
    
    for topic in topic_keywords:
        topic_keywords[topic] = list(set(topic_keywords[topic]))
    
    return topic_keywords

def clean_topic_list(df):
    stop_words = set(stopwords.words("english"))
    vague_topics = {
        "we", "who", "those", "the same time", "the community", "the documented benefits",
        "the most challenging and traumatic scenes"
    }

    def is_valid_topic(topic):
        words = topic.lower().split()
        if topic in vague_topics:
            return False
        if all(word in stop_words for word in words):
            return False
        return True

    cleaned_df = df[df["Topic"].apply(is_valid_topic)].reset_index(drop=True)
    return cleaned_df

def analyze_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    print("🔍 Loading NLP model...")
    nlp = spacy.load("en_core_web_sm")

    print("📑 Extracting regulatory sentences...")
    regulatory_sentences = extract_regulatory_sentences(text)

    print("🧠 Extracting topics and keywords...")
    topic_keywords = extract_topics_and_keywords(regulatory_sentences, nlp)

    print("\n✅ Regulated Topics and Their Keywords:\n")
    for topic, keywords in topic_keywords.items():
        print(f"🔹 Topic: {topic}")
        print(f"   Keywords: {', '.join(keywords)}\n")

    # Convert to DataFrame
    records = [{"Topic": topic, "Keywords": ", ".join(keywords)} for topic, keywords in topic_keywords.items()]
    df = pd.DataFrame(records)

    # Clean the topic list
    cleaned_df = clean_topic_list(df)

    # Make available in Spyder Variable Explorer
    ipython = get_ipython()
    if ipython:
        ipython.user_ns["regulation_df"] = cleaned_df
        
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud

    def visualize_topic_keywords(df):
        # Use Seaborn's whitegrid style
        sns.set(style="whitegrid")
    
        # Add Keyword Count Column
        df['KeywordCount'] = df['Keywords'].apply(lambda x: len(x.split(',')))

        # 🎯 Bar Chart
        plt.figure(figsize=(20, 10))
        plt.barh(df['Topic'], df['KeywordCount'], color='steelblue')
        plt.xlabel("Number of Keywords")
        plt.title("Top Regulatory Topics by Keyword Count")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

        # ☁️ Word Clouds for Each Topic
        for _, row in df.iterrows():
            topic = row['Topic']
            keywords = row['Keywords']
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(keywords)

            plt.figure(figsize=(8, 4))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f"Word Cloud: {topic}", fontsize=14)
            plt.tight_layout(pad=2)
            plt.show()

    print("📊 Cleaned Topics + Keywords DataFrame is now available as 'regulation_df' in Spyder.")
    visualize_topic_keywords(cleaned_df)

if __name__ == "__main__":
    filepath = "/Volumes/regulations_docket/mirrulations/specific/DEA-2024-0059/derived-data/mirrulations/extracted_txt/comments_extracted_text/pdfminer/DEA-2024-0059-0077_attachment_1_extracted.txt"
    analyze_file(filepath)


# %%


# # Optional: Convert Final Output to a DataFrame
# import pandas as pd

# def analyze_file(filepath):
#     with open(filepath, 'r', encoding='utf-8') as f:
#         text = f.read()

#     print("🔍 Loading NLP model...")
#     nlp = spacy.load("en_core_web_sm")

#     print("📑 Extracting regulatory sentences...")
#     regulatory_sentences = extract_regulatory_sentences(text)

#     print("🧠 Extracting topics and keywords...")
#     topic_keywords = extract_topics_and_keywords(regulatory_sentences, nlp)

#     print("\n✅ Regulated Topics and Their Keywords:\n")

#     # Create DataFrame for easier inspection/export
#     df = pd.DataFrame([
#         {"Topic": topic, "Keywords": ", ".join(keywords)}
#         for topic, keywords in topic_keywords.items()
#     ])
    
#     # Display in Variable Explorer
#     from IPython import get_ipython
#     get_ipython().user_ns["regulatory_df"] = df
    
#     print(df.to_string(index=False))  # still show in console
    
# filepath = "/Volumes/regulations_docket/mirrulations/specific/DEA-2024-0059/derived-data/mirrulations/extracted_txt/comments_extracted_text/pdfminer/DEA-2024-0059-5383_attachment_1_extracted.txt"
# analyze_file(filepath)
# %%