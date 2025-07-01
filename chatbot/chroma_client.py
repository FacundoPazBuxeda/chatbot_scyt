import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from backoffice.models import Evento, FAQ

# Ruta donde se almacenarán los vectores en disco
CHROMA_DIR = "chroma_store"

# Inicializar cliente persistente
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)

# Nombre de la colección
COLLECTION_NAME = "conocimiento"

# Embedding function explícita (opcional pero recomendado para claridad)
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")


def reindexar_base_conocimiento():
    print("🔄 Reindexando base de conocimiento...")

    # Si la colección ya existe, borrarla
    try:
        chroma_client.delete_collection(name=COLLECTION_NAME)
    except:
        pass

    # Crear colección con función de embeddings
    collection = chroma_client.create_collection(
        name=COLLECTION_NAME, embedding_function=embedding_fn
    )

    documentos = []
    metadatas = []
    ids = []

    # Eventos
    for evento in Evento.objects.select_related("categoria", "area").all():
        categoria = evento.categoria.nombre if evento.categoria else "Evento"
        texto = f"[{categoria.upper()}] {evento.titulo}\n{evento.cuerpo}"
        
        if evento.area:
            texto += f"\nÁrea responsable: {evento.area.nombre}"
            if evento.area.correo:
                texto += f"\nContacto: {evento.area.correo}"
        documentos.append(texto)
        metadatas.append({
            "tipo": "evento",
            "id": evento.id,
            "categoria": categoria
        })
        ids.append(f"evento-{evento.id}")

    # FAQs
    for faq in FAQ.objects.all():
        texto = f"{faq.pregunta}\n{faq.respuesta}"
        documentos.append(texto)
        metadatas.append({"tipo": "faq", "id": faq.id})
        ids.append(f"faq-{faq.id}")

    if documentos:
        collection.add(documents=documentos, metadatas=metadatas, ids=ids)
        print(f"✅ Se indexaron {len(documentos)} documentos.")
    else:
        print("⚠️ No hay documentos para indexar.")


def consultar_chroma(mensaje_usuario, k=3):
    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME, embedding_function=embedding_fn
    )
    resultados = collection.query(query_texts=[mensaje_usuario], n_results=k)

    documentos = resultados.get("documents", [])
    metadatas = resultados.get("metadatas", [])

    if documentos and metadatas:
        # Devuelve una lista de pares (texto, metadata)
        return list(zip(documentos[0], metadatas[0]))
    else:
        return []

