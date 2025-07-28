import pandas as pd
from bertopic import BERTopic
from collections import Counter
from transformers import pipeline

import torch
print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.cuda.get_device_name(0))


# Load cleaned comments
df = pd.read_csv('all_extracted_comments_cleaned.csv')

# Prepare data
docs = df['no_stopwords'].fillna("").tolist()

# Fit BERTopic
topic_model = BERTopic(nr_topics=10, verbose=True)
topics, _ = topic_model.fit_transform(docs)
df['related_topic'] = topics

# Collect most common tokens for each topic
topic_tokens = {}
for topic in set(topics):
    group_docs = df[df['related_topic'] == topic]['tokens'].explode().dropna().tolist()
    most_common_tokens = [word for word, count in Counter(group_docs).most_common(20)]
    topic_tokens[topic] = most_common_tokens

# Summarization pipeline
summarizer = pipeline("summarization", model="t5-small", device = 0)

topic_summaries = {}
for topic, keywords in topic_tokens.items():
    text = " ".join(keywords)
    prompt = f"Summarize: {text}"
    try:
        summary = summarizer(prompt, max_length=30, min_length=5, do_sample=False)
        topic_summaries[topic] = summary[0]['summary_text']
    except Exception as e:
        topic_summaries[topic] = "(summary failed)"
        print(f"Summary failed for topic {topic}: {e}")

# Map summary to each comment's topic
df['summary'] = df['related_topic'].map(topic_summaries)

df.to_csv('all_extracted_comments_topics_summaries.csv', index=False)
print("Step 2 complete! Output: all_extracted_comments_topics_summaries.csv")
