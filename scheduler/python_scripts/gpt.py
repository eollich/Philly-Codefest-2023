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



def query2(query_string):
    ai_key = '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'
    openai.api_key = ai_key
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=query_string,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0,
    )
    
    res = response.choices[0].text
    
    print(res)
    return res

def generateQueryString(title, description, role):
    return f'Generate an outline with the steps necessary to prepare for a meeting titled "{title}" with a description "{description}" for a "{role}". Provide output in only bullet points'
