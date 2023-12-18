
from flask import Flask, render_template, request, jsonify, send_file
import requests
import json
import os 

import pdfkit
import jinja2
import pickle


# Openai configuration
from pathlib import Path
from openai import OpenAI


# Module à propos du text 2 speech



app = Flask(__name__)


client = OpenAI(
    api_key=""
)


# Utilities functions


def generate_pdf(input, filename, persona_name, size):
    """
    Convertit un fichier HTML en PDF.

    :param html_file_path: Chemin vers le fichier HTML à convertir.
    :param output_pdf_path: Chemin où le PDF converti sera sauvegardé.
    """


    # Variables globales à utliser du template de base et le fichier output à utiliser en sortie
    html_file_path = 'template.html'
    output_pdf_path = f'./static/files/outputs/{filename}-{persona_name}.pdf'

    # Logique permettant de modifier le contenu du fichier html 
    # Et d'enregistrer ses modifications


    # Charger le template HTML avec jinja2
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'))
    template = env.get_template(html_file_path)

    # Intermediate html file
    intermediate_path = "./templates/intermediate.html"

    #modifier la font-size

    data = {
      "titre": input["titre"],
      "resume": input["resume"],
      "objet_du_litige": input["objet_du_litige"],
      "sens_de_la_decision" : input["sens_de_la_decision"],
      "motif_de_la_decision": input["motif_de_la_decision"],
      "font_size" : size * 35,
      "subtitle_font_size" : size * 30,
      "paragraph_font_size": size * 20,
    }

    # Remplir les placeholders avec les données
    html_content = template.render(data)

    # Enregistrer les modifications dans le fichier.
    with open(intermediate_path, 'w', encoding="utf-8") as file:
        file.write(html_content)

    try:
        pdfkit.from_file(intermediate_path, output_pdf_path, options={'encoding': 'UTF-8'})
        print(f"PDF généré avec succès : {output_pdf_path}")
    except Exception as e:
        print(f"Erreur lors de la conversion du fichier HTML en PDF : {e}")


# Appel vers la version open source de l'IA

def text_to_speech():
    pass


def text_to_speech_openai():
    pass


PERSONAS = ["Hugo", "Patrice", "Anna"]



@app.route("/", methods=['GET'])
def index():
    if request.args.get("name"):
        # Construction du chemin vers le fichier JSON
        name = request.args.get("name")
        json_file_path = os.path.join(app.static_folder, 'files', f"{name}.json")

        # Ouverture et lecture du fichier JSON
        data = pickle.load(open(f"./static/files/{name}.p", "rb"))
        input_data = {}
        for persona in PERSONAS:
            if persona == "Patrice" or persona == "Anna":
                size = 0.8
            else:
                size = 1.6
            input_data = {
                "resume": data["Resumé"][persona],
                "titre": data["Titre"],
                "objet_du_litige" : data["litige"][persona],
                "sens_de_la_decision": data["result"][persona],
                "motif_de_la_decision": data["motif"][persona],
                "size" : size
            }

            #generate_pdf(input_data, name, persona, size=input_data["size"])
            #text_to_speech_openai()

            # if persona == "Patrice":
            #     text_template_1 = f"""
            #        "Bonjour Patrice, cette décision concerne {data["Titre"]} et, en bref, ${data["Resumé"][persona]}."
            #     """
            #     text_template_2 = f"""
            #        Les raisons principales de cette décision sont liées à {data["litige"][persona]}. 
            #        En ce qui concerne le résultat, la décision a été {data["result"][persona]}.
            #     """
            #     text_template_3 = f"""
            #       Les motifs principaux de cette décision incluent {data["motif"][persona]}.
            #     """
            # elif persona == "Anna":
            #     text_template_1 = f"""
            #         "Bonjour Anna, La décision est à propos de {data["Titre"]}. En résumé, {data["Resumé"][persona]}."
            #     """
            #     text_template_2 = f"""
            #         Les raisons de cette décision sont : {data["litige"][persona]}. Ce que dit la décision, c'est {data["result"][persona]}. 
                    
            #     """
            #     text_template_3 = f"""
            #       Pourquoi cette décision a été prise : {data["motif"][persona]}.
            #     """
            # else :
            #     text_template_1 = f"""
            #         Hugo, cette information est sur {data["Titre"]}. Voici un résumé : {data["Resumé"][persona]}. 
            #     """
            #     text_template_2 = f"""
            #         La décision a été prise pour ces raisons : {data["litige"][persona]}. Ce que la décision veut dire : {data["result"][persona]}.
            #     """
            #     text_template_3 = f"""
            #        Pourquoi la décision a été prise : {data["motif"][persona]}.
            #     """
           
            # speech_file_path_1 = os.path.join(app.root_path, 'static', 'files', 'outputs', f"{name}_{persona}_1.mp3")
            # response = client.audio.speech.create(
            #     model="tts-1",
            #     voice="alloy",
            #     input=text_template_1
            # )
            # speech_file_path_2 = os.path.join(app.root_path, 'static', 'files', 'outputs', f"{name}_{persona}_2.mp3")
            # response = client.audio.speech.create(
            #     model="tts-1",
            #     voice="alloy",
            #     input=text_template_2
            # )
            # speech_file_path_3 = os.path.join(app.root_path, 'static', 'files', 'outputs', f"{name}_{persona}_3.mp3")
            # response = client.audio.speech.create(
            #     model="tts-1",
            #     voice="alloy",
            #     input=text_template_3
            # )
            # if os.path.exists(speech_file_path_1) and os.path.exists(speech_file_path_2) and  os.path.exists(speech_file_path_3):
            #     print(f"Ces audio existent déjà.")
            # else:
            #     response.stream_to_file(speech_file_path_1)
            #     response.stream_to_file(speech_file_path_2)
            #     response.stream_to_file(speech_file_path_3)
        # decisions = {
        #     "Decision01": "",
        #     "Decision02": "",
        #     "Decision03": ""
        # }
        # for element in decisions:
        #     decisions[name] = "selected"

        return render_template("index.html",name=name, default_pdf_url=f"files/outputs/{name}-Anna.pdf", default_audio_url=f"files/outputs/decision01-Anna.mp3", video_url=f"files/outputs/{name}_Anna.mp4")
    else:
        return "Please specify filename inside the URL"


# Get
@app.route("/data/<file_name>", methods=["GET"])
def get_data(file_name):
    persona = request.args.get("persona")
    endpoint_url = f"/data/{file_name}"
    decision_ul = f"/"
    audio_url = f"/static/files/outputs/{file_name}-{persona}.mp3"
    video_url = f"/static/files/outputs/{file_name}_{persona}.mp4"
    pdf_url = f"/static/files/outputs/{file_name}-{persona}.pdf"

    audio_file_name = f"{file_name}_{persona}"
    # Ajoutez l'attribut 'selected' à l'option correspondante
    options = {
        "Anna": "",
        "Hugo": "",
        "Patrice": ""
    }

    # decisions = {
    #     "Decision01": "",
    #     "Decision02": "",
    #     "Decision03": ""
    # }

    for person in options:
        options[persona] = "selected"

    # for element in decisions:
    #     decisions[file_name] = "selected"
    
    output = f"""
       <div class="output-section">


        <div class="form-select">
            <label>Décision:</label>
             <select name="name" id="decision_select">
               <option value="Decision01">Decision 01</option>
               <option value="Decision02">Decision 02</option>
               <option value="Decision03">Decision 03</option>
          </select>
        </div><br>

        <div class="form-select">
              <label>Persona:</label>
            <select name="persona" id="persona-select" hx-get="{endpoint_url}" hx-trigger="change" hx-target="#container">
               <option value="Anna" {options['Anna']}>Anna</option>
               <option value="Hugo" {options['Hugo']}>Hugo</option>
               <option value="Patrice" {options['Patrice']}>Patrice</option>
            </select>
        </div>

            <audio id="audioPlayer" src="{audio_url}" filename="{audio_file_name}" controls>
                <a href="{audio_url}">
                   Télécharger l'audio
                </a>
            </audio>
            <!-- PDF Reader -->
              <object 
              data="{pdf_url}"
              type="application/pdf"
              width="900"
              height="678"
              id  = "pdf-container"
              >
                <iframe 
                  src="{pdf_url}" 
                   width="900"
                   height="678"
                   >
                   <p>This browser does not support PDF!</p>
                </iframe>
              </object><br></br>
            <video id="videoPlayer" width="640" height="360" controls>
                <source id="videoSource" src="{video_url}" type="video/mp4">
                Votre navigateur ne supporte pas les vidéos HTML5.
            </video>
            <!-- Possible download button -->
        </div>
     """
    return output


if __name__ == "__main":
    app.run(debug=True)