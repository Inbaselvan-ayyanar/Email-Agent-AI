def summarize(text):
    
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

    tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
    model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
    inputs = tokenizer(text, max_length=1024, truncation=True, return_tensors="pt")
    summary_ids = model.generate(inputs['input_ids'], max_length=1300, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary
    '''response = ollama.chat(model="mistral", messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": f"provide a explainable and grammertically correct text for the given query {summary}"}
    ])
    return response['message']['content']'''


def generate_email(text, subject):
    import ollama
    if len(text)>5000:
        text=summarize(text)
    prompt = (
        f"You received an email with the following details:\n\n"
        f"Subject: {subject}\n"
        f"Summary of the email content: {text}\n\n"
        f"Write a reply email that is:\n"
        f"- Professional\n"
        f"-Polite and clear\n"
        f"-Relevant to the email content\n"
        f"- Written in a natural human tone\n\n"
        f"Do not include any placeholders like [Your Name]; generate a complete, ready-to-send email."
        
    )

    try:
        response = ollama.chat(model="mistral", messages=[
            {"role": "system", "content": "You are an AI assistant skilled in writing high-quality professional emails."},
            {"role": "user", "content": prompt}
        ])
        return response['message']['content']
    except Exception as e:
        return f"An error occurred while generating the email: {str(e)}"