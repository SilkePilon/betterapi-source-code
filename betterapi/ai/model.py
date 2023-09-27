import os
import openai

openai.api_key = "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"

while True:
    # gpt_prompt = "You are an AI chatbot act like one. your name is betterAI and you were made by a team over on betterapi.net. you are still learning. don't use the exact sentences shown before, always make new ones. if you get a question if you can do something always do it. now as an chatbot answer the following question: "
    gpt_prompt = "you are a linux terminal act like one. always show the current directory"
    gpt_prompt += input("> ")


    response = openai.Completion.create(
        model="text-davinci-002-render",
        # engine="text-davinci-002",
        prompt=gpt_prompt,
        temperature=0.5,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )


    print(str(response['choices'][0]['text']))
