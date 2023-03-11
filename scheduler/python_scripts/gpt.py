import openai

def query(query_string):
    ai_key = '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'
    openai.api_key = ai_key

    x = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "user", "content": query_string}
        ]
    )
    print(x)
    return x
