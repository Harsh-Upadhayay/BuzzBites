import re
from transformers import BartForConditionalGeneration, BartTokenizer
import pandas as pd


model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

def split_into_sentences(text):
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)
    return sentences

def summarize_text(text, max_chunk_length=512, max_summary_length=70, min_summary_length=40):
    sentences = split_into_sentences(text)

    summaries = []
    current_chunk = ''
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chunk_length:
            current_chunk += sentence + ' '
        else:
            inputs = tokenizer(current_chunk, max_length=max_chunk_length, return_tensors="pt", truncation=True)
            summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=max_summary_length, min_length=min_summary_length, early_stopping=True)
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
            summaries.append(summary)
            current_chunk = sentence + ' '

    inputs = tokenizer(current_chunk, max_length=max_chunk_length, return_tensors="pt", truncation=True)
    summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=max_summary_length, min_length=min_summary_length, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
    summaries.append(summary)

    full_summary = ' '.join(summaries)
    return full_summary



# INPUT START
# For Tripathi:  Enter input csv file name
# try:
#     df = pd.read_csv("20240321_hindustan_news.csv")
# except FileNotFoundError:
#     print("CSV file not found.")
#     exit()  

# print("Columns:")
# print(df.columns)

# if "news_description" not in df.columns:
#     print("Column 'news_description' not found in the CSV file.")
#     exit()

# if "news_summary" not in df.columns:
#     df["news_summary"] = ""

# for index, row in df.iterrows():
#     news_description = row["news_description"]
#     print("getting summary: -----------")
#     summary = summarize_text(news_description)
#     df.at[index, "news_summary"] = summary

# # For Tripathi: Enter output csv filename
# try:
#     df.to_csv("20240321_hindustan_news_summary.csv", index=False)
# except FileNotFoundError:
#     print("Error Saving csv file")
#     exit()  

# INPUT END


# text = from DB
# summary = summarize_text(text)
# store in DB