import nltk
import streamlit as st
import speech_recognition as sr
from nltk.chat.util import Chat, reflections

# Charger le fichier texte de questions-réponses
def load_qa_file(file_path):
    qa_pairs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.read().strip().split('\n\n')
            for line in lines:
                q_and_a = line.split('\n')
                question = q_and_a[0].strip()
                answers = [answer.strip() for answer in q_and_a[1:]]
                qa_pairs.append((question, answers))
    except FileNotFoundError:
        st.write("Le fichier de questions-réponses n'a pas été trouvé.")
    return qa_pairs

# Fonction pour transcrire la parole en texte
def transcribe_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Dites quelque chose...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language='fr-FR')
        return text
    except sr.UnknownValueError:
        st.write("Impossible de comprendre l'audio")
        return ""
    except sr.RequestError as e:
        st.write(f"Erreur lors de la demande de reconnaissance vocale : {e}")
        return ""

# Fonction principale pour gérer les entrées de l'utilisateur
def main():
    st.title("Chatbot avec reconnaissance vocale")
    user_input = st.text_input("Entrez votre message")

    # Charger le fichier de questions-réponses
    qa_file = 'football_info_fr.txt'  # Assurez-vous que le chemin est correct
    qa_pairs = load_qa_file(qa_file)

    # Création de l'objet Chat à partir des paires définies
    chatbot = Chat(qa_pairs, reflections)

    if st.button("Valider"):
        if user_input:
            response = chatbot.respond(user_input)
            st.write(f"Chatbot : {response}")

    if st.button("Microphone"):
        spoken_input = transcribe_speech()
        st.write(f"Vous avez dit : {spoken_input}")
        response = chatbot.respond(spoken_input)
        st.write(f"Chatbot : {response}")

    if st.button("Réinitialiser"):
        # Réinitialiser les champs de saisie
        st.text_input("Entrez votre message", value="", key="reset_input")
        # Réinitialiser la valeur de user_input
        user_input = ""
        # Recharger l'application
        st.experimental_rerun()

# Point d'entrée pour l'exécution de l'application Streamlit
if __name__ == "__main__":
    main()
