import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Memoria entre sesiones
MEMORY_FILE = "memory.json"

def cargar_memoria() -> dict:
    """Carga el banco y estado recordados de la sesion anterior."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"banco": None, "estado": None, "routing": None}

def guardar_memoria(estado: dict) -> None:
    """Guarda banco y estado para la proxima sesion."""
    with open(MEMORY_FILE, "w") as f:
        json.dump({
            "banco":   estado["banco"],
            "estado":  estado["estado"],
            "routing": estado["routing"]
        }, f)

# API-KEY Gemini
load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# Tabla de routing numbers por banco y estado
ROUTING_TABLE = {
    ("bank of america", "texas"):      "111000025",
    ("bank of america", "california"): "121000358",
    ("bank of america", "florida"):    "063100277",
    ("chase", "texas"):                "111000614",
    ("chase", "california"):           "322271627",
    ("chase", "florida"):              "267084131",
    ("wells fargo", "texas"):          "111900659",
    ("wells fargo", "california"):     "121042882",
    ("citibank", "texas"):             "113193532",
    ("citibank", "new york"):          "021000089",
    ("citibank", "florida"):           "266086554",
    ("td bank", "florida"):            "067014822",
    ("td bank", "new york"):           "026013673",
    ("td bank", "new jersey"):         "031201360",
}

# Códigos de error Nacha y sus mensajes amigables
NACHA_ERRORS = {
    "R01": (
        "No tienes fondos suficientes en tu cuenta para completar esta "
        "transferencia. Por favor verifica tu saldo e intenta de nuevo."
    ),
    "R03": (
        "No encontramos una cuenta activa con los datos que ingresaste. "
        "Por favor revisa tu numero de cuenta y routing number."
    ),
    "R10": (
        "La transaccion no fue autorizada por tu banco. "
        "Por favor contactanos para verificar tu informacion."
    ),
}

# System prompt con instrucciones claras para el agente
SYSTEM_PROMPT = """
Eres un asistente virtual de Insights Wealth Management, especializado en 
ayudar a clientes a fondear su cuenta de inversiones via ACH. Tu tono debe 
ser amigable y formal.

REGLA OBLIGATORIA:
Antes de dar cualquier informacion, SIEMPRE debes preguntar primero el banco 
y el estado del cliente. Sin estos dos datos no puedes continuar.

FLUJO DE PREGUNTAS (en este orden estricto):
1. En que banco tienes tu cuenta?
2. En que estado abriste esa cuenta?
   El sistema inferira el routing number automaticamente.
   Muestraselo al cliente y pidele confirmacion.
   Si no lo reconoce, pidele que lo verifique en su app bancaria.
3. Cuanto deseas depositar? (minimo $1, maximo $25,000)
4. Lo necesitas estandar (1-3 dias habiles) o urgente (mismo dia)?
5. Cual es tu numero de cuenta bancaria?
6. Es una cuenta checking o savings?

Con todos los datos completos, guia al cliente paso a paso para completar 
el deposito desde su banco.

MANEJO DE FALLOS:
- R01: fondos insuficientes, pidele que verifique saldo e intente de nuevo
- R03: cuenta invalida, pidele que revise sus datos bancarios
- R10: no autorizado, escala al equipo de soporte de Insights

PREGUNTAS FUERA DE ALCANCE:
Responde: No tengo esa informacion en mi sistema en este momento, disculpe.

DISCLAIMER (mencionar antes de pedir datos bancarios):
Recuerde que sus datos estan protegidos bajo los estandares de seguridad 
de Insights Wealth Management. Nunca compartiremos su informacion con terceros.
"""

#Función para inferir routing number basado en banco y estado
def lookup_routing(banco: str, estado: str) -> str | None:
    key = (banco.lower().strip(), estado.lower().strip())
    return ROUTING_TABLE.get(key)

# Funcion para detectar errores Nacha en el mensaje del usuario
def detectar_error_nacha(mensaje: str) -> str | None:
    for codigo in NACHA_ERRORS:
        if codigo in mensaje.upper():
            return codigo
    return None

# Agente principal
def ejecutar_agente():
    print("\n" + "="*55)
    print("   Insights WM - Asistente de Fondeo ACH")
    print("="*55)
    print("Escribe 'salir' para terminar la conversacion.\n")

    # Inicializar chat con historial
    chat = client.chats.create(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )

    # Cargar memoria de sesion anterior
    estado = cargar_memoria()

    # Mensaje de bienvenida — si hay memoria, el agente lo sabe
    if estado["banco"] and estado["estado"]:
        print(f"[Memoria: banco={estado['banco'].title()}, estado={estado['estado'].title()}]\n")
        bienvenida = chat.send_message(
            f"El cliente regresa. Recuerdas que su banco es {estado['banco'].title()} "
            f"en {estado['estado'].title()}. Saludalo, mencionale que recuerdas sus datos "
            f"y preguntale cuanto desea depositar esta vez."
        )
    else:
        bienvenida = chat.send_message(
            "El cliente acaba de iniciar una conversacion. "
            "Saludalo y preguntale en que banco tiene su cuenta."
        )
    print(f"Agente: {bienvenida.text}\n")

    # Loop conversacional
    while True:
        usuario = input("Tu: ").strip()

        if usuario.lower() == "salir":
            guardar_memoria(estado)
            print("\nAgente: Hasta luego! Fue un placer ayudarte.")
            break

        if not usuario:
            continue

        # Detectar error Nacha en el mensaje del usuario
        error = detectar_error_nacha(usuario)
        if error:
            print(f"\nAgente: {NACHA_ERRORS[error]}\n")
            continue

        # Actualizar estado si el usuario menciona banco o estado
        palabras = usuario.lower()
        for banco in ["bank of america", "chase", "wells fargo", "citibank", "td bank"]:
            if banco in palabras:
                estado["banco"] = banco
        for est in ["texas", "california", "florida", "new york", "new jersey"]:
            if est in palabras:
                estado["estado"] = est

        # Enriquecer el mensaje si tenemos banco y estado pero no routing aun
        mensaje_enriquecido = usuario
        if estado["banco"] and estado["estado"] and not estado["routing"]:
            routing = lookup_routing(estado["banco"], estado["estado"])
            if routing:
                estado["routing"] = routing
                mensaje_enriquecido = (
                    f"{usuario}\n\n[Sistema: El routing number inferido para "
                    f"{estado['banco'].title()} en {estado['estado'].title()} "
                    f"es {routing}. Comunicaselo al cliente y pidele confirmacion.]"
                )

        # Enviar al modelo y mostrar respuesta
        respuesta = chat.send_message(mensaje_enriquecido)
        print(f"\nAgente: {respuesta.text}\n")


if __name__ == "__main__":
    ejecutar_agente()