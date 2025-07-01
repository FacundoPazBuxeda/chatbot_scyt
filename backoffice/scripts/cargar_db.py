from backoffice.models import Categoria, Area, Evento, FAQ
from datetime import date, timedelta
import random

# Limpiar datos anteriores (opcional)
Categoria.objects.all().delete()
Area.objects.all().delete()
Evento.objects.all().delete()
FAQ.objects.all().delete()

categorias = {
    "Charla": Categoria.objects.create(nombre="Charla"),
    "Taller": Categoria.objects.create(nombre="Taller"),
    "Curso": Categoria.objects.create(nombre="Curso"),
    "Capacitación": Categoria.objects.create(nombre="Capacitación"),
    "Convocatoria": Categoria.objects.create(nombre="Convocatoria"),
    "Evento General": Categoria.objects.create(nombre="Evento General"),
}

areas = {"Educación": Area.objects.create(nombre="Área de Educación", correo="educacion@ejemplo.gob"), "Tecnología": Area.objects.create(nombre="Área de Tecnología", correo="tecnologia@ejemplo.gob"), "Emprendedores": Area.objects.create(nombre="Área de Emprendedores", correo="emprendedores@ejemplo.gob"), "Juventud": Area.objects.create(nombre="Área de Juventud", correo="juventud@ejemplo.gob"),
}

# Crear eventos
def crear_evento(titulo, cuerpo, categoria, area, dias_offset):
    Evento.objects.create(
        titulo=titulo,
        cuerpo=cuerpo,
        categoria=categorias[categoria],
        area=areas[area],
        fecha=date.today() + timedelta(days=dias_offset)
    )

crear_evento(
    "Charla sobre Inteligencia Artificial",
    "📅 15 de agosto, 18 hs\n📍 Nodo Tecnológico\n👤 Diserta: Dra. Ana Suárez\nTema: Introducción a la IA en la educación.",
    "Charla", "Tecnología", 3
)

crear_evento(
    "Taller de Robótica para Jóvenes",
    "📅 20 de agosto, 9 a 13 hs\n📍 Aula Maker\n👨‍🏫 Coordina: Ing. Pablo Ruiz\n🎯 Traer notebook propia. Cupos limitados.",
    "Taller", "Juventud", 7
)

crear_evento(
    "Curso de Programación Web",
    "📅 Del 1 al 30 de septiembre\n📍 Aula Virtual\n👩‍🏫 Docentes: Laura Gómez y Marcos Ledesma\n✅ Requiere conocimientos básicos de informática.",
    "Curso", "Educación", 20
)

crear_evento(
    "Capacitación en Comunicación Pública",
    "📅 12 y 13 de septiembre\n📍 Salón de conferencias\n🎓 Destinado a personal administrativo y comunicadores del Estado.",
    "Capacitación", "Educación", 25
)

crear_evento(
    "Convocatoria a Becas de Innovación 2025",
    "📅 Inscripción: 1 al 15 de agosto\n📌 Fases: evaluación técnica, entrevista y publicación de seleccionados\n📄 Info: becas.innovacion.gob.ar",
    "Convocatoria", "Tecnología", -2
)

crear_evento(
    "Fiesta de la Ciencia",
    "📅 10 de septiembre, de 16 a 22 hs\n📍 Parque del Encuentro\n🎪 Stands interactivos, shows musicales y feria gastronómica.",
    "Evento General", "Tecnología", 30
)

crear_evento(
    "Charla: Mujeres en Tecnología",
    "📅 28 de agosto, 10 hs\n📍 Auditorio Nodo\n👤 Diserta: Lic. Valeria Ponce\n🎯 Cómo fomentar la inclusión en carreras tecnológicas.",
    "Charla", "Tecnología", 10
)

crear_evento(
    "Taller de Escritura Creativa",
    "📅 5 y 6 de septiembre, 15 a 18 hs\n📍 Biblioteca Central\n🧠 Actividades prácticas y lectura compartida.",
    "Taller", "Emprendedores", 22
)

crear_evento(
    "Curso intensivo de Excel",
    "📅 2 al 10 de octubre\n📍 Aula 2, Centro de Formación\n💻 Nivel inicial y certificado al finalizar.",
    "Curso", "Educación", 50
)

crear_evento(
    "Concurso: Jóvenes Innovadores 2025",
    "📅 Postulación hasta el 5 de septiembre\n🎯 Presentá tu idea tecnológica y participá por premios.\n📍 Más info en juventud.gob.ar",
    "Convocatoria", "Juventud", 15
)

crear_evento(
    "Capacitación en Gestión de Emprendimientos",
    "📅 18 y 19 de septiembre, de 9 a 13 hs\n📍 Coworking ACTI\n👩‍🏫 Facilitadora: Lic. Daniela Núñez\n🎓 Público objetivo: emprendedores y pequeños negocios\n✅ Incluye material digital y certificado digital\n📌 Inscripción gratuita en gestionemprende.acti.gob.ar",
    "Capacitación", "Educación", 35
)

crear_evento(
    "Charla: Emprender con Impacto",
    "📅 25 de septiembre, 17 hs\n📍 SUM CreaLab\n👤 Diserta: Ing. Rodrigo Figueroa\n🌱 Temas: sostenibilidad, triple impacto y nuevos modelos de negocio\n💡 Incluye espacio de networking post-charla.",
    "Charla", "Emprendedores", 42
)

crear_evento(
    "Feria de Innovación y Tecnología",
    "📅 15 de octubre, de 14 a 21 hs\n📍 Espacio Multieventos ECEI\n🎪 Exhibición de proyectos tecnológicos, robótica, impresión 3D y domótica\n🎤 Presentaciones en vivo, sorteos y charlas relámpago durante la jornada\n✅ Entrada libre y gratuita\n📧 Contacto: ecei@ejemplo.gob",
    "Evento General", "Emprendedores", 65
)

crear_evento(
    "Taller Práctico: Diseño de Proyectos Culturales",
    "📅 6 y 7 de octubre, de 15 a 19 hs\n📍 Casa de la Cultura\n🛠 Requisitos: traer notebook y una idea de proyecto propia\n👩‍🏫 Coordina: Mg. Alejandra Ibarra\n🎯 Ejercicios prácticos y análisis de casos reales\n📌 Certificado de participación para quienes completen el 100% del taller.",
    "Taller", "Emprendedores", 55
)

# Crear FAQs
FAQ.objects.create(pregunta="¿Dónde queda el Nodo Tecnológico?", respuesta="En Av. Núñez del Prado s/n, cerca del Parque Industrial.")
FAQ.objects.create(pregunta="¿Los cursos son gratuitos?", respuesta="Sí, la mayoría son sin costo, pero requieren inscripción previa.")
FAQ.objects.create(pregunta="¿Puedo asistir sin inscripción?", respuesta="Algunos eventos son libres, pero los talleres y cursos suelen requerir inscripción.")
FAQ.objects.create(pregunta="¿Cómo obtengo certificado?", respuesta="Debés cumplir el 80% de asistencia y completar una evaluación final.")
FAQ.objects.create(pregunta="¿Hay edad mínima para participar?", respuesta="Sí, en general es para mayores de 16 años. Se indica en cada evento.")
FAQ.objects.create(pregunta="¿Cómo me contacto con un área específica?", respuesta="Consultá los correos institucionales en la sección Áreas del sitio.")
FAQ.objects.create(pregunta="¿Qué debo llevar a un taller práctico?", respuesta="Generalmente se requiere traer notebook y materiales básicos. Cada taller lo especifica en su descripción.")
FAQ.objects.create(pregunta="¿Qué pasa si no puedo asistir a todos los días de un curso?", respuesta="Podés asistir parcialmente, pero para obtener el certificado se suele exigir un mínimo de asistencia del 80%.")
FAQ.objects.create(pregunta="¿Dónde me inscribo a las capacitaciones?", respuesta="Cada capacitación incluye un enlace o correo de inscripción. Revisá el detalle completo en la descripción del evento.")

print("Proceso TERMINADO")