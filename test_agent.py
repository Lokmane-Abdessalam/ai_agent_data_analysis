import re
import time

from langchain_core.messages import HumanMessage, SystemMessage

# Import du superviseur depuis votre backend
from supervisor import superviseur, system_prompt


def lire_cahier_de_test(chemin_fichier="questions_de_test.md"):
    """Analyse le fichier Markdown et extrait les tests à effectuer."""
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    # On découpe le fichier par les titres (## Test...)
    blocs_tests = contenu.split("## Test")[1:]
    tests = []

    for bloc in blocs_tests:
        nom_test = bloc.split("\n")[0].strip()

        # Expressions régulières adaptées au format actuel du fichier Markdown.
        match_question = re.search(
            r'\*\s+\*\*Question à poser\s*:\*\*\s*\n?\s*>\s*"([^"]+)"',
            bloc,
        )
        match_outils = re.search(r'\*\s+\*\*Outils déclenchés\s*:\*\*(.+)', bloc)

        if match_question and match_outils:
            question = match_question.group(1)
            ligne_outils = match_outils.group(1)
            outils_attendus = re.findall(r'`([^`]+)`', ligne_outils)

            tests.append(
                {
                    "nom": nom_test,
                    "question": question,
                    "outils_attendus": set(outils_attendus),
                }
            )
        else:
            print(
                f"Avertissement : Le test '{nom_test}' a été ignoré car son "
                "formatage n'est pas reconnu."
            )

    return tests


def evaluer_agent():
    print("Démarrage de la campagne de tests automatisés...")
    tests = lire_cahier_de_test()

    # Sécurité anti-crash si aucun test n'est trouvé
    if len(tests) == 0:
        print(
            "\nERREUR : Aucun test valide trouvé dans le fichier Markdown. "
            "Vérifiez le format."
        )
        return

    tests_reussis = 0

    for i, test in enumerate(tests, 1):
        print("\n==========================================")
        print(f"EXÉCUTION DU TEST {i} : {test['nom']}")
        print(f"Question : {test['question']}")

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=test["question"]),
        ]

        debut = time.time()
        try:
            resultat = superviseur.invoke({"messages": messages})
        except Exception as e:
            print(f"ÉCHEC FATAL : Erreur technique de l'agent ({e})")
            continue
        fin = time.time()

        outils_utilises = set()
        for message in resultat["messages"]:
            if hasattr(message, "tool_calls") and message.tool_calls:
                for tool_call in message.tool_calls:
                    outils_utilises.add(tool_call["name"])

        print(f"Temps de réponse : {round(fin - debut, 2)} secondes")
        print(f"Outils attendus : {test['outils_attendus']}")
        print(f"Outils utilisés : {outils_utilises}")

        if outils_utilises == test["outils_attendus"]:
            print("RÉSULTAT : SUCCÈS")
            tests_reussis += 1
        else:
            print("RÉSULTAT : ÉCHEC (Mauvaise sélection d'outils)")
            print(
                "Réponse générée par l'IA :\n"
                f"{resultat['messages'][-1].content}"
            )

    print("\nCAMPAGNE TERMINÉE")
    pourcentage_reussite = (tests_reussis / len(tests)) * 100
    print(
        f"Score de réussite : {tests_reussis} / {len(tests)} "
        f"({pourcentage_reussite:.0f}%)"
    )


if __name__ == "__main__":
    evaluer_agent()
