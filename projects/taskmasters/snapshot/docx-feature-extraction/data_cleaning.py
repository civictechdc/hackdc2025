import pandas as pd
import re
from nltk.corpus import stopwords
import nltk

# Uncomment the line below and run once if you haven't already:
# nltk.download('stopwords')

# Load your data
df = pd.read_csv('all_extracted_comments.csv')

# Get English stopwords
stop_words = set(stopwords.words('english'))

def basic_clean(text):
    """Lowercase, remove punctuation/numbers, and extra spaces."""
    if pd.isnull(text):
        return ''
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)      # Remove punctuation and numbers
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

def remove_stopwords(text):
    """Remove stopwords from a space-separated string."""
    tokens = text.split()
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(filtered_tokens)

def tokenize(text):
    """Split text into tokens (words)."""
    return text.split()

# Apply the functions in sequence:
df['cleaned_comment'] = df['comment_text'].apply(basic_clean)
df['no_stopwords'] = df['cleaned_comment'].apply(remove_stopwords)
df['tokens'] = df['no_stopwords'].apply(tokenize)

# Save to new CSV
df.to_csv('all_extracted_comments_cleaned.csv', index=False)

print("Cleaning complete! Saved to all_extracted_comments_cleaned.csv")
