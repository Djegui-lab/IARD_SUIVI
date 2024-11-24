import streamlit as st
import psycopg2
from psycopg2.extras import Json
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy import create_engine
import numpy as np


import os
import os
import streamlit as st

# Afficher les valeurs des variables d'environnement (pour le debug)
st.write(f"APP_PASSWORD: {os.getenv('APP_PASSWORD')}")
st.write(f"DEVELOPER_NAME: {os.getenv('DEVELOPER_NAME')}")

# Récupérer les valeurs sensibles
PASSWORD = os.getenv("APP_PASSWORD")
DEVELOPER_NAME = os.getenv("DEVELOPER_NAME")

# Vérification stricte en production
if not PASSWORD or not DEVELOPER_NAME:
    st.error("⚠️ Les variables d'environnement `APP_PASSWORD` et `DEVELOPER_NAME` doivent être configurées.")
    st.stop()

# Gestion des sessions utilisateur
if "auth_success" not in st.session_state:
    st.session_state.auth_success = False

# Authentification
if not st.session_state.auth_success:
    st.markdown(f"""
    ### 🔐 **Application Sécurisée**
    Cette application a été développée par **{DEVELOPER_NAME}** pour garantir une gestion des données optimale et sécurisée.  
    🚨 *Veuillez saisir le mot de passe fourni par le développeur pour accéder à l'application.* 🚨
    """)
    st.subheader("🔒 Authentification")
    password_input = st.text_input("🔑 Saisissez votre mot de passe :", type="password")
    if st.button("🔓 Se connecter"):
        if password_input == PASSWORD:
            st.session_state.auth_success = True
            st.success("✅ Connexion réussie ! Bienvenue.")
        else:
            st.error("❌ Mot de passe incorrect. Veuillez réessayer.")
    # Arrêter ici si non authentifié
    st.stop()

# Contenu principal de l'application (uniquement accessible après authentification)
st.success("🎉 Vous êtes connecté avec succès.")
st.write("Bienvenue dans l'application sécurisée.")
st.header("📊 Tableau de Bord")
st.write("Ajoutez ici vos fonctionnalités et visualisations principales.")
if st.button("🚪 Se déconnecter"):
    st.session_state.auth_success = False




DATABASE_URL= os.getenv('DATABASE_URL')

# Fonction pour créer la table
def create_table():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS suivi_dossiers (
            id SERIAL PRIMARY KEY,
            date_heure TIMESTAMP NOT NULL,
            civilite VARCHAR(10),
            nom_prenom VARCHAR(255),
            mail_client VARCHAR(255),
            type_mail VARCHAR(50),
            telephone_client VARCHAR(15),
            courtier VARCHAR(255),
            motif_resiliation VARCHAR(100),
            formule VARCHAR(100),
            mensualite DECIMAL(10, 2),
            compagnie VARCHAR(255),
            note TEXT,
            statut_souscription VARCHAR(50),
            numero_contrat VARCHAR(100),
            date_souscription DATE,
            date_debut_couverture DATE,
            date_expiration DATE,
            documents_requis VARCHAR(100),
            documents_fournis VARCHAR(100),
            statut_documents VARCHAR(50),
            relance_client BOOLEAN,
            date_relance DATE,
            statut_validation_compagnie VARCHAR(50),
            date_contact_client DATE,
            type_contact VARCHAR(50),
            resultat_contact TEXT
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
        return "Table créée avec succès."
    except Exception as e:
        return f"Erreur lors de la création de la table : {e}"

# Fonction pour insérer les données
def insert_data(data):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO suivi_dossiers (
            date_heure, civilite, nom_prenom, mail_client, type_mail, telephone_client,courtier, motif_resiliation, 
            formule, mensualite, compagnie, note, statut_souscription, numero_contrat, 
            date_souscription, date_debut_couverture, date_expiration, documents_requis, 
            documents_fournis, statut_documents, relance_client, date_relance, statut_validation_compagnie, 
            date_contact_client, type_contact, resultat_contact)
        VALUES (
            %(date_heure)s, %(civilite)s, %(nom_prenom)s, %(mail_client)s, %(type_mail)s, %(telephone_client)s, %(courtier)s, 
            %(motif_resiliation)s, %(formule)s, %(mensualite)s, %(compagnie)s, %(note)s, %(statut_souscription)s, 
            %(numero_contrat)s, %(date_souscription)s, %(date_debut_couverture)s, %(date_expiration)s, 
            %(documents_requis)s, %(documents_fournis)s, %(statut_documents)s, %(relance_client)s, 
            %(date_relance)s, %(statut_validation_compagnie)s, %(date_contact_client)s, %(type_contact)s, 
            %(resultat_contact)s
        );
        """
       
        cursor.execute(insert_query, data)
        conn.commit()
        cursor.close()
        conn.close()
        return "Données insérées avec succès."
    except Exception as e:
        return f"Erreur lors de l'insertion des données : {e}"





# Connexion à PostgreSQL avec SQLAlchemy
# Fonction pour récupérer des données depuis la base de données
DATABASE_URLS = os.getenv('DATABASE_URLS')

engine = create_engine(DATABASE_URLS)

def fetch_data(query_filter=None):
    try:
        # Construire la requête SQL
        base_query = "SELECT * FROM suivi_dossiers"
        
        if query_filter:
            base_query += f" WHERE {query_filter}"

        # Lire les données via pandas
        df = pd.read_sql_query(base_query, engine)
        
        return df

    except Exception as e:
        print(f"Erreur lors de la récupération des données : {e}")
        return pd.DataFrame()











# Style de l'application
st.title("🚗 Gestion des Dossiers Clients 🚀")
st.markdown("""
<div style="text-align: center; font-size: 18px;">
    Bienvenue dans l'outil de suivi des dossiers clients. <br>
    Gérez efficacement vos informations grâce à cette interface intuitive.
</div>
""", unsafe_allow_html=True)

st.image("https://via.placeholder.com/800x200?text=Votre+Logo+Ici", use_container_width=True)

# Formulaire pour saisir les informations client
st.subheader("📋 Remplissez les informations du client")

col1, col2 = st.columns(2)

with st.form(key="client_form"):
    with col1:
        civilite = st.selectbox('Civilité', ['M.', 'Mme'], help="Choisissez la civilité du client")
        nom_prenom = st.text_input('Nom et Prénom', help="Entrez le nom complet du client")
        mail_client = st.text_input('Email du client', help="Entrez l'adresse email du client")
        type_mail = st.selectbox('Type de contact', ['Email', 'Téléphone'])
        telephone_client = st.text_input("Téléphone du client", value=None)
        courtier = st.text_input('Courtier', help="Nom du courtier responsable")
        motif_resiliation = st.selectbox('Motif de résiliation', ['Non-paiement', 'Sinistre', 'Autre'])
        formule = st.text_input('Formule', help="Indiquez la formule choisie")
        mensualite = st.number_input('Mensualité (€)', min_value=0.0, format="%.2f")

    with col2:
        compagnie = st.text_input("Compagnie d'assurance", help="Nom de la compagnie d'assurance")
        note = st.text_area('Note', help="Ajoutez une note supplémentaire")
        statut_souscription = st.selectbox('Statut de souscription', ['En attente', 'Souscrit', 'Refusé'])
        numero_contrat = st.text_input('Numéro de contrat')
        date_souscription = st.date_input("Date de souscription", value=None)
        date_debut_couverture = st.date_input('Date de début de couverture', value=None)
        date_expiration = st.date_input('Date d\'expiration',value=None)
        


    documents_requis = st.text_area('Documents requis (séparés par des virgules)')
    documents_fournis = st.text_area('Documents fournis (séparés par des virgules)')
    statut_documents = st.selectbox('Statut des documents', ['Complet', 'Partiellement complet', 'Non fourni'])

    submit_button = st.form_submit_button("📤 Soumettre les données")

# Créer la table si elle n'existe pas
create_table_result = create_table()
st.write(create_table_result)

if submit_button:
    data = {
        "date_heure": datetime.now(),
        "civilite": civilite,
        "nom_prenom": nom_prenom,
        "mail_client": mail_client,
        "type_mail": type_mail,
        "telephone_client": telephone_client,
        "courtier": courtier,
        "motif_resiliation": motif_resiliation,
        "formule": formule,
        "mensualite": mensualite,
        "compagnie": compagnie,
        "note": note,
        "statut_souscription": statut_souscription,
        "numero_contrat": numero_contrat,
        "date_souscription": date_souscription,
        "date_debut_couverture": date_debut_couverture,
        "date_expiration": date_expiration,
        "documents_requis": documents_requis.split(","),
        "documents_fournis": documents_fournis.split(","),
        "statut_documents": statut_documents,
        "relance_client": False,
        "date_relance": None,
        "statut_validation_compagnie": "En attente",
        "date_contact_client": None,
        "type_contact": None,
        "resultat_contact": None
    }
    insert_result = insert_data(data)
    st.success(insert_result)






st.subheader("🔍 Filtrer les dossiers clients")

# Saisie directe de filtres SQL avec un exemple comme placeholder
query_filter = st.text_input(
    "Entrez un filtre SQL",
    placeholder="Exemple : statut_souscription = 'Souscrit' OR mensualite > 50"
)

# Validation et exécution du filtre
if query_filter:
    # Validation simple : interdiction des mots-clés sensibles
    invalid_keywords = ["DELETE", "DROP", "UPDATE", ";"]
    if any(keyword in query_filter.upper() for keyword in invalid_keywords):
        st.error("Requête invalide : des mots-clés non autorisés sont détectés.")
        filtered_data = pd.DataFrame()  # Pas de chargement si requête invalide
    else:
        try:
            # Exécuter la requête SQL
            filtered_data = fetch_data(query_filter)
        except Exception as e:
            st.error(f"Erreur dans la requête SQL : {e}")
            filtered_data = pd.DataFrame()
else:
    # Chargement des données sans filtre
    filtered_data = fetch_data()

# Affichage des données
st.write("## Données enregistrées")
if not filtered_data.empty:
    # Affichage interactif des données
    st.dataframe(
        filtered_data,
        width=1000,
        height=500,
        use_container_width=True
    )
else:
    st.warning("Aucune donnée correspondant au filtre.")








# Connexion à la base de données (modifiez DATABASE_URL selon vos paramètres)
#DATABASE_URL = "votre_url_base_de_donnees"

# Fonction pour récupérer les données du client
def get_client_data(mail_client):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cursor = conn.cursor()
        
        query = "SELECT * FROM suivi_dossiers WHERE mail_client = %s;"
        cursor.execute(query, (mail_client,))
        column_names = [desc[0] for desc in cursor.description]
        client_data = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if client_data:
            return dict(zip(column_names, client_data))
        else:
            return None
    except psycopg2.Error as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour mettre à jour les données du client
def update_data(mail_client, updated_data):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cursor = conn.cursor()

        update_query = """
        UPDATE suivi_dossiers
        SET 
            civilite = %(civilite)s,
            nom_prenom = %(nom_prenom)s,
            type_mail = %(type_mail)s,
            courtier = %(courtier)s,
            motif_resiliation = %(motif_resiliation)s,
            formule = %(formule)s,
            mensualite = %(mensualite)s,
            compagnie = %(compagnie)s,
            note = %(note)s,
            statut_souscription = %(statut_souscription)s,
            numero_contrat = %(numero_contrat)s,
            date_souscription = %(date_souscription)s,
            date_debut_couverture = %(date_debut_couverture)s,
            date_expiration = %(date_expiration)s,
            documents_requis = %(documents_requis)s,
            documents_fournis = %(documents_fournis)s,
            statut_documents = %(statut_documents)s,
            date_relance = %(date_relance)s,
            statut_validation_compagnie = %(statut_validation_compagnie)s,
            date_contact_client = %(date_contact_client)s,
            type_contact = %(type_contact)s,
            resultat_contact = %(resultat_contact)s
        WHERE mail_client = %(mail_client)s;
        """
        updated_data['mail_client'] = mail_client
        cursor.execute(update_query, updated_data)
        conn.commit()

        cursor.close()
        conn.close()
        return "Mise à jour réussie."
    except psycopg2.Error as e:
        return f"Erreur lors de la mise à jour : {e}"

# Barre latérale pour saisir l'email du client
st.sidebar.header("🔄 Mise à jour des données")
mail_client = st.sidebar.text_input("Email du client", help="Entrez l'adresse email du client existant.")

# Pré-remplir les données du client si un email est saisi
client_data = get_client_data(mail_client) if mail_client else None

# Initialiser les données par défaut ou celles du client
if client_data:
    initial_data = {
        "civilite": client_data["civilite"] if client_data else "M.",
        "nom_prenom": client_data["nom_prenom"] if client_data else "",
        "type_mail": client_data["type_mail"] if client_data else "Email",
        "courtier": client_data["courtier"] if client_data else "",
        "motif_resiliation": client_data["motif_resiliation"] if client_data else "Non-paiement",
        "formule": client_data["formule"] if client_data else "",
        "mensualite": client_data["mensualite"] if client_data else 0.0,
        "compagnie": client_data["compagnie"] if client_data else "",
        "note": client_data["note"] if client_data else "",
        "statut_souscription": client_data["statut_souscription"] if client_data else "En attente",
        "numero_contrat": client_data["numero_contrat"] if client_data else "",
        "date_souscription": client_data["date_souscription"] if client_data else datetime.now().date(),
        "date_debut_couverture": client_data["date_debut_couverture"] if client_data else datetime.now().date(),
        "date_expiration": client_data["date_expiration"] if client_data else datetime(2025, 11, 1).date(),
        "documents_requis": client_data["documents_requis"] if client_data else "",
        "documents_fournis": client_data["documents_fournis"] if client_data else "",
        "statut_documents": client_data["statut_documents"] if client_data else "Non fourni",
        "date_relance": client_data["date_relance"] if client_data else datetime.now().date(),
        "statut_validation_compagnie": client_data["statut_validation_compagnie"] if client_data else "Non validé",
        "date_contact_client": client_data["date_contact_client"] if client_data else datetime.now().date(),
        "type_contact": client_data["type_contact"] if client_data else "Email",
        "resultat_contact": client_data["resultat_contact"] if client_data else "Non contacté"
    }
else:
    initial_data = {
        "civilite": "M.",
        "nom_prenom": "",
        "type_mail": "Email",
        "courtier": "",
        "motif_resiliation": "Non-paiement",
        "formule": "",
        "mensualite": 0.0,
        "compagnie": "",
        "note": "",
        "statut_souscription": "En attente",
        "numero_contrat": "",
        "date_souscription": datetime.now().date(),
        "date_debut_couverture": datetime.now().date(),
        "date_expiration": datetime(2025, 11, 1).date(),
        "documents_requis": "",
        "documents_fournis": "",
        "statut_documents": "Non fourni",
        "date_relance": datetime.now().date(),
        "statut_validation_compagnie": "Non validé",
        "date_contact_client": datetime.now().date(),
        "type_contact": "Email",
        "resultat_contact": "Non contacté"
    }
# Vérification et récupération des valeurs avec des valeurs par défaut
def get_initial_value(key, options=None, default=None):
    """
    Récupère la valeur initiale avec une vérification des options valides.
    Si la valeur n'est pas dans les options ou absente, retourne la valeur par défaut.
    """
    value = initial_data.get(key, default)
    if options and value not in options:
        return default
    return value

# Formulaire de mise à jour des données
with st.sidebar.form(key="update_form"):
    civilite_options = ["M.", "Mme"]
    civilite = st.selectbox("Civilité", civilite_options, index=civilite_options.index(get_initial_value("civilite", civilite_options, "M.")))

    nom_prenom = st.text_input("Nom et Prénom", value=initial_data.get("nom_prenom", ""))

    type_mail_options = ["Email", "Téléphone"]
    type_mail = st.selectbox("Type de contact", type_mail_options, index=type_mail_options.index(get_initial_value("type_mail", type_mail_options, "Email")))
    telephone_client = st.text_input("Téléphone du client", value=initial_data.get("telephone_client", ""))

    courtier = st.text_input("Courtier", value=initial_data.get("courtier", ""))

    motif_resiliation_options = ["Non-paiement", "Sinistre", "Autre"]
    motif_resiliation = st.selectbox(
        "Motif de résiliation",
        motif_resiliation_options,
        index=motif_resiliation_options.index(get_initial_value("motif_resiliation", motif_resiliation_options, "Autre"))
    )

    formule = st.text_input("Formule", value=initial_data.get("formule", ""))

    mensualite = st.number_input("Mensualité (€)", min_value=0.0, format="%.2f", value=float(initial_data.get("mensualite", 0.0)))

    compagnie = st.text_input("Compagnie d'assurance", value=initial_data.get("compagnie", ""))

    note = st.text_area("Note", value=initial_data.get("note", ""))

    statut_souscription_options = ["En attente", "Souscrit", "Refusé"]
    statut_souscription = st.selectbox(
        "Statut de souscription",
        statut_souscription_options,
        index=statut_souscription_options.index(get_initial_value("statut_souscription", statut_souscription_options, "En attente"))
    )

    numero_contrat = st.text_input("Numéro de contrat", value=initial_data.get("numero_contrat", ""))

    # Champs de date avec des valeurs par défaut
    date_souscription = st.date_input("Date de souscription", value=initial_data.get("date_souscription", None))
    date_debut_couverture = st.date_input("Date de début de couverture", value=initial_data.get("date_debut_couverture", None))
    date_expiration = st.date_input("Date d'expiration", value=initial_data.get("date_expiration", None))

    documents_requis = st.text_area("Documents requis", value=initial_data.get("documents_requis", ""))
    documents_fournis = st.text_area("Documents fournis", value=initial_data.get("documents_fournis", ""))

    statut_documents_options = ["Complet", "Partiellement complet", "Non fourni"]
    statut_documents = st.selectbox(
        "Statut des documents",
        statut_documents_options,
        index=statut_documents_options.index(get_initial_value("statut_documents", statut_documents_options, "Non fourni"))
    )

    date_relance = st.date_input("Date de relance", value=initial_data.get("date_relance", None))

    statut_validation_options = ["Validé", "Non validé", "En attente"]
    statut_validation_compagnie = st.selectbox(
        "Statut de validation de la compagnie",
        statut_validation_options,
        index=statut_validation_options.index(get_initial_value("statut_validation_compagnie", statut_validation_options, "En attente"))
    )

    date_contact_client = st.date_input("Date de contact avec le client", value=initial_data.get("date_contact_client", None))

    type_contact_options = ["Email", "Téléphone"]
    type_contact = st.selectbox(
        "Type de contact",
        type_contact_options,
        index=type_contact_options.index(get_initial_value("type_contact", type_contact_options, "Email")),
        key="type_contact_key"
    )

    resultat_contact_options = ["Contacté", "Non contacté", "Refusé"]
    resultat_contact = st.selectbox(
        "Résultat du contact",
        resultat_contact_options,
        index=resultat_contact_options.index(get_initial_value("resultat_contact", resultat_contact_options, "Non contacté")),
        key="resultat_contact_key"
    )

    # Soumettre le formulaire
    submit_button = st.form_submit_button("Mettre à jour les données")

    if submit_button:
        updated_data = {
            "civilite": civilite,
            "nom_prenom": nom_prenom,
            "type_mail": type_mail,
            "courtier": courtier,
            "motif_resiliation": motif_resiliation,
            "formule": formule,
            "mensualite": mensualite,
            "compagnie": compagnie,
            "note": note,
            "statut_souscription": statut_souscription,
            "numero_contrat": numero_contrat,
            "date_souscription": date_souscription,
            "date_debut_couverture": date_debut_couverture,
            "date_expiration": date_expiration,
            "documents_requis": documents_requis,
            "documents_fournis": documents_fournis,
            "statut_documents": statut_documents,
            "date_relance": date_relance,
            "statut_validation_compagnie": statut_validation_compagnie,
            "date_contact_client": date_contact_client,
            "type_contact": type_contact,
            "resultat_contact": resultat_contact
        }

        # Mise à jour des données
        result = update_data(mail_client, updated_data)
        st.success(result)




def delete_row(row_id):
    """Supprime une ligne de la table par son ID."""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cursor = conn.cursor()
        delete_query = "DELETE FROM suivi_dossiers WHERE id = %s"
        cursor.execute(delete_query, (row_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return f"Ligne avec ID {row_id} supprimée avec succès."
    except Exception as e:
        return f"Erreur lors de la suppression de la ligne : {e}"

st.subheader("🗑️ Supprimer une ligne")

# Formulaire pour la suppression
with st.form("delete_form"):
    row_id_to_delete = st.number_input("Entrez l'ID de la ligne à supprimer", min_value=1, step=1, format="%d")
    delete_submit = st.form_submit_button("Supprimer")

# Si l'utilisateur clique sur "Supprimer"
if delete_submit:
    # Récupérer les données actuelles
    filtered_data = fetch_data()
    
    # Vérifier si l'ID existe dans les données
    if row_id_to_delete in filtered_data['id'].values:  # Remplacez 'id' par le nom exact de votre colonne d'ID
        delete_message = delete_row(row_id_to_delete)  # Appelle la fonction pour supprimer la ligne
        st.success(delete_message)  # Affiche un message de succès
        
        # Recharger et afficher les données mises à jour après suppression
        filtered_data = fetch_data()
        st.write("## Données mises à jour")
        st.dataframe(filtered_data)
    else:
        st.error(f"L'ID {row_id_to_delete} n'existe pas dans les données.")






# Connexion à la base de données avec SQLAlchemy
#DATABASE_URL = "postgres://user:password@host:port/database"
#engine = create_engine(DATABASE_URL)



def modify_data(client_id=None, client_email=None, statut_souscription=None, courtier=None):
    try:
        # Si on passe un ID ou un email, on met à jour ce client spécifique
        if client_id:
            query = text("""
                UPDATE suivi_dossiers 
                SET statut_souscription = :statut_souscription, courtier = :courtier
                WHERE id = :client_id
            """)
            params = {"client_id": client_id, "statut_souscription": statut_souscription, "courtier": courtier}
        elif client_email:
            query = text("""
                UPDATE suivi_dossiers 
                SET statut_souscription = :statut_souscription, courtier = :courtier
                WHERE email = :client_email
            """)
            params = {"client_email": client_email, "statut_souscription": statut_souscription, "courtier": courtier}
        else:
            st.warning("⚠️ Veuillez fournir soit un ID client soit un email.")
            return
        
        # Connexion à la base de données et exécution de la requête
        with engine.connect() as conn:
            conn.execute(query, params)
            conn.commit()
        
        # Message de succès
        st.success(f"✅ Le statut de souscription et le courtier ont été mis à jour avec succès ! 🎉")
    
    except Exception as e:
        # Message d'erreur en cas de problème
        st.error(f"❌ Erreur lors de la modification des données : {e}")

# Interface Streamlit pour que l'utilisateur puisse saisir un ID client, un email et le nom du courtier
st.title("🔄 Mise à jour du statut de souscription des clients")

# Disposition en 2 colonnes pour optimiser l'espace
col1, col2 = st.columns(2)

with col1:
    client_id = st.text_input("🆔 ID du client (facultatif)", "")
    client_email = st.text_input("📧 Email du client (facultatif)", "")

with col2:
    statut_souscription = st.selectbox("📝 Nouveau statut de souscription", ["Souscrit", "Non souscrit", "En attente"])
    courtier = st.text_input("💼 Nom du courtier", "")

# Vérification et bouton pour soumettre
if st.button("✅ Mettre à jour le statut et le courtier"):
    if (client_id or client_email) and courtier:  # Vérifier si au moins un des champs ID/email et le courtier sont remplis
        if statut_souscription:
            modify_data(client_id=client_id if client_id else None, 
                        client_email=client_email if client_email else None, 
                        statut_souscription=statut_souscription,
                        courtier=courtier)
        else:
            st.warning("⚠️ Veuillez choisir un statut de souscription.")
    else:
        st.warning("⚠️ Veuillez fournir soit un ID client soit un email, ainsi qu'un nom de courtier.")






# Formulaire de filtrage des statuts des documents avec une présentation plus attrayante
st.subheader("🔍 Filtrer les dossiers clients par statut des documents")

# Ajouter des descriptions plus visuelles avec des emojis pour chaque statut
status_options = {
    "Complet": "✅ Documents complets (permis, carte grise, etc.)",
    "Partiellement complet": "⚠️ Documents partiellement fournis (manque des pièces)",
    "Non fourni": "❌ Aucun document fourni (pas de permis, carte grise, etc.)"
}

# Sélection multiple pour les statuts des documents avec descriptions
statut_selections = st.multiselect(
    "Choisissez les statuts des documents à filtrer",
    options=list(status_options.keys()),
    format_func=lambda x: status_options[x],  # Affiche les descriptions
    default=['Partiellement complet', 'Non fourni']  # Sélection par défaut
)

# Bouton pour appliquer le filtre avec une clé unique
if st.button('Appliquer le filtre 🔍', key='filtrer_statut_documents'):
    # Construire le filtre SQL en fonction des statuts sélectionnés
    if statut_selections:
        statut_filter = f"statut_documents IN ({', '.join([repr(status) for status in statut_selections])})"
    else:
        statut_filter = None  # Si aucun statut sélectionné, ne pas appliquer de filtre

    # Récupérer les données filtrées
    filtered_data = fetch_data(statut_filter)

    # Afficher les résultats filtrés avec un joli tableau et un message plus attrayant
    st.write("## Données enregistrées 📑")

    if not filtered_data.empty:
        st.dataframe(filtered_data)
    else:
        st.warning("🚫 Aucune donnée correspondant au filtre sélectionné.")







