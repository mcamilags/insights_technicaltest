import os
import re
import json
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

# -- Memoria entre sesiones ----------------------------------------------------
MEMORY_FILE = "memory.json"
TRANSCRIPT_FILE = "transcripcion.txt"

def cargar_memoria() -> dict:
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"nombre": None, "banco": None, "estado": None, "routing": None}

def guardar_memoria(estado: dict) -> None:
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "nombre":  estado["nombre"],
            "banco":   estado["banco"],
            "estado":  estado["estado"],
            "routing": estado["routing"]
        }, f)

def limpiar_memoria() -> dict:
    estado_vacio = {"nombre": None, "banco": None, "estado": None, "routing": None}
    guardar_memoria(estado_vacio)
    return estado_vacio

# -- Transcripcion -------------------------------------------------------------
transcripcion_sesion = []

def log(rol: str, texto: str):
    """Guarda una linea en la transcripcion y la imprime en consola."""
    linea = f"{rol}: {texto}"
    transcripcion_sesion.append(linea)
    print(f"\n{linea}\n")

def guardar_transcripcion(escenario: str = ""):
    """Guarda la transcripcion de la sesion en transcripcion.txt."""
    with open(TRANSCRIPT_FILE, "a", encoding="utf-8") as f:
        f.write("\n" + "="*55 + "\n")
        f.write(f"SESION: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if escenario:
            f.write(f" | {escenario}")
        f.write("\n" + "="*55 + "\n")
        for linea in transcripcion_sesion:
            f.write(linea + "\n")
        f.write("\n")

# -- API Key -------------------------------------------------------------------
load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# -- Tabla de routing numbers --------------------------------------------------
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

# -- Normalizacion de nombres de banco ----------------------------------------
BANK_ALIASES = {
    "bofa":             "bank of america",
    "bac":              "bank of america",
    "bank america":     "bank of america",
    "bankofamerica":    "bank of america",
    "jp morgan":        "chase",
    "jpmorgan":         "chase",
    "chase bank":       "chase",
    "wellsfargo":       "wells fargo",
    "wells":            "wells fargo",
    "wf":               "wells fargo",
    "citi":             "citibank",
    "citigroup":        "citibank",
    "td":               "td bank",
    "toronto dominion": "td bank",
}

def normalizar_banco(texto: str) -> str | None:
    texto = texto.lower().strip()
    for banco in ["bank of america", "chase", "wells fargo", "citibank", "td bank"]:
        if banco in texto:
            return banco
    for alias, nombre in BANK_ALIASES.items():
        if alias in texto:
            return nombre
    return None

# -- Validacion de monto -------------------------------------------------------
MONTO_MIN = 1
MONTO_MAX = 25000

def validar_monto(texto: str) -> tuple[float | None, str | None]:
    limpio = texto.replace("$", "").replace(",", "").strip()
    try:
        monto = float(limpio)
    except ValueError:
        return None, "No pude reconocer ese monto. Por favor ingresa un numero (ejemplo: 5000)."
    if monto < MONTO_MIN:
        return None, f"El monto minimo para depositar es ${MONTO_MIN}."
    if monto > MONTO_MAX:
        return None, f"El monto maximo por transaccion es ${MONTO_MAX:,}. Por favor ingresa un monto menor."
    return monto, None

# -- Codigos de error Nacha ----------------------------------------------------
NACHA_ERRORS = {
    "R01": (
        "Fondos insuficientes: tu banco rechazo la transferencia porque no "
        "habia saldo suficiente. Por favor verifica tu saldo e intentalo de nuevo."
    ),
    "R03": (
        "Cuenta invalida: no encontramos una cuenta activa con los datos que "
        "ingresaste. Por favor revisa tu numero de cuenta y routing number."
    ),
    "R10": (
        "Debito no autorizado: tu banco indico que esta transaccion no fue "
        "autorizada. Por favor contactanos para verificar tu informacion."
    ),
}

def detectar_error_nacha(mensaje: str) -> str | None:
    for codigo in NACHA_ERRORS:
        if codigo in mensaje.upper():
            return codigo
    return None

# -- System prompt -------------------------------------------------------------
SYSTEM_PROMPT = """
Eres un asistente virtual de Insights Wealth Management, especializado en 
ayudar a clientes a fondear su cuenta de inversiones via ACH. Tu tono debe 
ser amigable y formal, como un asesor que quiere ayudar pero que tambien 
transmite confianza y seguridad.

ANTES DE COMENZAR:
0. Pregunta el nombre del cliente y usalo durante toda la conversacion.
   Si el cliente regresa y ya tienes su nombre en memoria, saludalo por su 
   nombre sin volver a preguntarlo.

REGLA OBLIGATORIA:
Antes de dar cualquier informacion, SIEMPRE debes preguntar primero el banco 
y el estado del cliente. Sin estos dos datos no puedes continuar.

FLUJO DE PREGUNTAS (en este orden estricto):
1. En que banco tienes tu cuenta?
2. En que estado abriste esa cuenta?
   Con banco + estado, infiere el routing number de la tabla interna.
   Muestraselo al cliente y pidele confirmacion.
   Si no lo reconoce, pidele que lo verifique en su app bancaria.
3. Cuanto deseas depositar?
   Valida que el monto sea mayor a $0 y no supere $25,000 por transaccion.
   El sistema validara el monto. Si hay error, comunica y vuelve a pedir.
4. Lo necesitas estandar (1-3 dias habiles) o urgente (mismo dia)?
5. Cual es tu numero de cuenta bancaria?
6. Es una cuenta checking o savings?

Cuando el sistema te entregue el resumen de confirmacion, presentaselo 
al cliente claramente usando su nombre y pide su confirmacion antes de proceder.

LOGICA DE ROUTING:
Cuando el cliente te diga su banco y estado, busca en esta tabla:

| Banco            | Estado     | Routing Number |
|------------------|------------|----------------|
| Bank of America  | Texas      | 111000025      |
| Bank of America  | California | 121000358      |
| Bank of America  | Florida    | 063100277      |
| Chase            | Texas      | 111000614      |
| Chase            | California | 322271627      |
| Chase            | Florida    | 267084131      |
| Wells Fargo      | Texas      | 111900659      |
| Wells Fargo      | California | 121042882      |
| Citibank         | Texas      | 113193532      |
| Citibank         | New York   | 021000089      |
| Citibank         | Florida    | 266086554      |
| TD Bank          | Florida    | 067014822      |
| TD Bank          | New York   | 026013673      |
| TD Bank          | New Jersey | 031201360      |

Si el banco o estado no esta en la tabla, pide al cliente que verifique 
su routing number en su app bancaria o en la parte inferior de un cheque.

MANEJO DE FALLOS:
- R01: fondos insuficientes, pidele que verifique saldo e intente de nuevo
- R03: cuenta invalida, pidele que revise sus datos bancarios
- R10: no autorizado, escala al equipo de soporte de Insights

PREGUNTAS FUERA DE ALCANCE:
Responde: No tengo esa informacion en mi sistema en este momento, disculpe.
En que mas puedo ayudarte con tu deposito?

DISCLAIMER (mencionar antes de pedir el numero de cuenta):
Recuerde que sus datos estan protegidos bajo los estandares de seguridad 
de Insights Wealth Management. Nunca compartiremos su informacion con terceros.
"""

# -- Inferir routing -----------------------------------------------------------
def lookup_routing(banco: str, estado: str) -> str | None:
    key = (banco.lower().strip(), estado.lower().strip())
    return ROUTING_TABLE.get(key)

# -- Resumen de confirmacion ---------------------------------------------------
def generar_resumen(estado: dict, monto: float, urgencia: str,
                    cuenta: str, tipo_cuenta: str) -> str:
    nombre = estado["nombre"].title() if estado["nombre"] else "cliente"
    return (
        f"[Sistema: Resumen de la operacion para confirmar con {nombre}:\n"
        f"  Banco:     {estado['banco'].title()}\n"
        f"  Estado:    {estado['estado'].title()}\n"
        f"  Routing:   {estado['routing']}\n"
        f"  Cuenta:    {cuenta}\n"
        f"  Tipo:      {tipo_cuenta}\n"
        f"  Monto:     ${monto:,.2f}\n"
        f"  Velocidad: {'Urgente (mismo dia)' if urgencia == 'urgente' else 'Estandar (1-3 dias habiles)'}\n"
        f"Presenta este resumen a {nombre} y pregunta si confirma para proceder.]"
    )

# -- Agente principal ----------------------------------------------------------
def ejecutar_agente():
    print("\n" + "="*55)
    print("   Insights WM - Asistente de Fondeo ACH")
    print("="*55)
    print("Escribe 'salir' para terminar | 'reset' para limpiar memoria")
    escenario = input("Nombre del escenario (ej: Exito, R01, R03): ").strip()
    print()

    chat = client.chats.create(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )

    estado = cargar_memoria()
    tx = {"monto": None, "urgencia": None, "cuenta": None,
          "tipo": None, "esperando_monto": False}

    # Bienvenida personalizada segun memoria
    if estado["nombre"] and estado["banco"] and estado["estado"]:
        prompt_bienvenida = (
            f"El cliente {estado['nombre'].title()} regresa. Ya sabes que su banco es "
            f"{estado['banco'].title()} en {estado['estado'].title()}. "
            f"Saludalo por su nombre, menciona que recuerdas sus datos bancarios "
            f"y preguntale cuanto desea depositar esta vez."
        )
    elif estado["nombre"]:
        prompt_bienvenida = (
            f"El cliente {estado['nombre'].title()} regresa. "
            f"Saludalo por su nombre y preguntale en que banco tiene su cuenta."
        )
    else:
        prompt_bienvenida = (
            "El cliente acaba de iniciar una conversacion. "
            "Saludalo y preguntale su nombre."
        )

    bienvenida = chat.send_message(prompt_bienvenida)
    log("Agente", bienvenida.text)

    # Loop conversacional
    while True:
        usuario = input("Tu: ").strip()

        if not usuario:
            continue

        transcripcion_sesion.append(f"Tu: {usuario}")

        # Salir
        if usuario.lower() == "salir":
            guardar_memoria(estado)
            nombre = estado["nombre"].title() if estado["nombre"] else ""
            despedida = f"Hasta luego{', ' + nombre if nombre else ''}! Fue un placer ayudarte en Insights WM."
            log("Agente", despedida)
            guardar_transcripcion(escenario)
            print(f"[Transcripcion guardada en {TRANSCRIPT_FILE}]")
            break

        # Reset
        if usuario.lower() == "reset":
            estado = limpiar_memoria()
            tx = {"monto": None, "urgencia": None, "cuenta": None,
                  "tipo": None, "esperando_monto": False}
            reinicio = chat.send_message(
                "El cliente quiere iniciar una nueva operacion desde cero. "
                "Saludalo y preguntale su nombre."
            )
            log("Agente", reinicio.text)
            continue

        # Detectar error Nacha
        error = detectar_error_nacha(usuario)
        if error:
            log("Agente", NACHA_ERRORS[error])
            continue

        # Capturar nombre si aun no lo tenemos
        if not estado["nombre"]:
            nombre_limpio = usuario.strip().split()[0]
            if len(nombre_limpio) > 1 and nombre_limpio.isalpha():
                estado["nombre"] = nombre_limpio.lower()

        # Normalizar banco
        banco_detectado = normalizar_banco(usuario)
        if banco_detectado:
            estado["banco"] = banco_detectado

        # Detectar estado
        for est in ["texas", "california", "florida", "new york", "new jersey"]:
            if est in usuario.lower():
                estado["estado"] = est

        # Validar monto
        mensaje_enriquecido = usuario
        if tx["esperando_monto"]:
            monto, error_monto = validar_monto(usuario)
            if error_monto:
                log("Agente", error_monto)
                continue
            else:
                tx["monto"] = monto
                tx["esperando_monto"] = False
                mensaje_enriquecido = (
                    f"{usuario}\n\n[Sistema: Monto validado: ${monto:,.2f}. Continua con el flujo.]"
                )
        elif not tx["monto"] and estado["routing"]:
            monto, error_monto = validar_monto(usuario)
            if monto:
                tx["monto"] = monto
                mensaje_enriquecido = (
                    f"{usuario}\n\n[Sistema: Monto validado: ${monto:,.2f}. Continua con el flujo.]"
                )
            elif any(c.isdigit() for c in usuario):
                log("Agente", error_monto)
                tx["esperando_monto"] = True
                continue

        # Detectar urgencia
        if "urgente" in usuario.lower():
            tx["urgencia"] = "urgente"
        elif "estandar" in usuario.lower() or "standard" in usuario.lower():
            tx["urgencia"] = "estandar"

        # Detectar tipo de cuenta
        if "checking" in usuario.lower():
            tx["tipo"] = "checking"
        elif "savings" in usuario.lower() or "ahorros" in usuario.lower():
            tx["tipo"] = "savings"

        # Detectar numero de cuenta
        numeros = re.findall(r'\b\d{8,12}\b', usuario)
        if numeros and not tx["cuenta"]:
            tx["cuenta"] = numeros[0]

        # Inferir routing
        if estado["banco"] and estado["estado"] and not estado["routing"]:
            routing = lookup_routing(estado["banco"], estado["estado"])
            if routing:
                estado["routing"] = routing
                mensaje_enriquecido = (
                    f"{usuario}\n\n[Sistema: Routing number inferido para "
                    f"{estado['banco'].title()} en {estado['estado'].title()}: "
                    f"{routing}. Muestraselo al cliente y pidele confirmacion.]"
                )

        # Resumen cuando tenemos todos los datos
        if (tx["monto"] and tx["urgencia"] and tx["cuenta"] and
                tx["tipo"] and estado["routing"]):
            mensaje_enriquecido = generar_resumen(
                estado, tx["monto"], tx["urgencia"], tx["cuenta"], tx["tipo"]
            )
            tx = {"monto": None, "urgencia": None, "cuenta": None,
                  "tipo": None, "esperando_monto": False}

        # Enviar al modelo
        respuesta = chat.send_message(mensaje_enriquecido)
        log("Agente", respuesta.text)



if __name__ == "__main__":
    ejecutar_agente()