# pip install openai
# pip install gradio

from openai import OpenAI
from google.colab import userdata
import gradio as gr

client = OpenAI(api_key = userdata.get('OPENAI_KEY'))

behaviour_prompt = "Eres un profesor de informática. Respondes con energía y ganas de que tus alumnos aprendan. Si te preguntan por algo ajeno a esta materia, intentas reorientar la conversación a tu materia"

def predict(message, history):
  history_openai_format = [{"role":'system', 'content':behaviour_prompt}]

  for human, assistant in history:
    history_openai_format.append({"role": "user", "content": human })
    history_openai_format.append({"role": "assistant", "content":assistant})

  history_openai_format.append({"role": "user", "content": message})


  response = client.chat.completions.create(
              model='gpt-3.5-turbo',
              messages=history_openai_format,
              temperature=1.0,
              stream=True)

  partial_message= ''
  for chunk in response:
    if chunk.choices[0].delta.content is not None:
      partial_message = partial_message + chunk.choices[0].delta.content
      yield partial_message

custom_css='footer {visibility: hidden}'

def check_auth(username, password):
  return password=='pass1234'

gr.ChatInterface(fn=predict,
                 title='aitiMENTOR',
                 theme=gr.themes.Soft(),
                 stop_btn=None,
                 retry_btn=None,
                 undo_btn=None,
                 clear_btn=None,
                 css=custom_css).queue().launch(debug=True, auth=check_auth)
