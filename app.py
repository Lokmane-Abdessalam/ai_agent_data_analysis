import streamlit as st
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# On importe votre agent et son prompt depuis votre backend
from supervisor import superviseur, system_prompt

# 1. Configuration de la page Web
st.set_page_config(
    page_title="Executive AI - Direction", 
    page_icon="👔", 
    layout="centered"
)

st.title("👔 Assistant Stratégique de Direction")
st.markdown("Interrogez vos bases de ventes et vos rapports stratégiques en langage naturel.")

# 2. Initialisation de la mémoire de l'Agent (Session State)
if "messages_agent" not in st.session_state:
    # L'agent a toujours besoin de son SystemPrompt en premier
    st.session_state.messages_agent = [SystemMessage(content=system_prompt)]
    
# 3. Initialisation de l'historique visuel (Ce que l'utilisateur voit)
if "messages_ui" not in st.session_state:
    st.session_state.messages_ui = [
        {"role": "assistant", "content": "Bonjour. Je suis connecté à la base de données et aux documents stratégiques. Que souhaitez-vous analyser ?"}
    ]

# 4. Affichage de l'historique de conversation
for msg in st.session_state.messages_ui:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Barre de saisie utilisateur
if prompt := st.chat_input("Ex: Quel est le CA en France et pourquoi a-t-il baissé ?"):
    
    # A. On affiche immédiatement la question à l'écran
    st.chat_message("user").markdown(prompt)
    st.session_state.messages_ui.append({"role": "user", "content": prompt})
    
    # B. On l'ajoute à la mémoire technique de l'agent
    st.session_state.messages_agent.append(HumanMessage(content=prompt))

    # C. On fait réfléchir l'Agent (avec un indicateur de chargement)
    with st.chat_message("assistant"):
        with st.spinner("Recherche dans les bases SQL et les documents RAG en cours..."):
            try:
                # Appel de votre agent LangGraph
                resultat = superviseur.invoke({"messages": st.session_state.messages_agent})
                
                # Extraction de la réponse finale
                reponse_ia = resultat["messages"][-1].content
                
                # Affichage à l'écran
                st.markdown(reponse_ia)
                
                # Sauvegarde dans les historiques
                st.session_state.messages_ui.append({"role": "assistant", "content": reponse_ia})
                st.session_state.messages_agent.append(AIMessage(content=reponse_ia))
                
            except Exception as e:
                st.error(f"Une erreur technique est survenue : {e}")