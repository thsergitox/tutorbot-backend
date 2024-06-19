import json
from groq import Groq

from config import settings


class GroqConnection:
    client = Groq(
        api_key=settings.GROQ_API_KEY
    )

    def generate_exam(self, num_preg, topic):
        """
        Esta función es el punto de entrada principal de la aplicación. Configura el cliente, la interfaz de Streamlit, y maneja la interacción con el chatbot.
        """

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f'Genera una examen con {num_preg} preguntas de' + topic + ', esas preguntas son objetos en este formato {"question": "","options": [],"answer": ""} los cuales estan guardados en un array generando un array de objetos, el formato de Respuesta debe ser el numero de la posicion del array de Preguntas',
                }
            ],
            model="llama3-8b-8192",
        )
        ret = chat_completion.choices[0].message.content

        ok_first = True
        ini = end = -1

        for i, e in enumerate(ret):
            if e == '[' and ok_first:
                ok_first = False
                ini = i
            if e == ']':
                end = i
        jsonString = ret[ini:end + 1]
        y = json.loads(jsonString)
        result_json_str = json.dumps(y, ensure_ascii=False, separators=(',', ':'))

        return result_json_str

    def ask_groq(self, answer):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f'Hola soy ricardo, ayudame con esta consulta: {answer}',
                }
            ],
            model="llama3-8b-8192",
        )
        ret = chat_completion.choices[0].message.content

        return ret



groqConnection = GroqConnection()
