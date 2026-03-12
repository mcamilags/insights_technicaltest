# Prueba Técnica — Analista Jr. de Inversiones

**Insights Wealth Management | Marzo 2026**

---

## Descripción

Evaluación técnica para el rol de Analista Jr. de Inversiones en Insights Wealth Management, una plataforma de gestión patrimonial enfocada en clientes latinoamericanos en los Estados Unidos. El proyecto abarca cuatro ejercicios progresivos: diseño de consultas de datos, análisis cuantitativo de portafolios, automatización de decisiones y desarrollo de un agente conversacional con IA.

---

## Estructura del Proyecto

```
insights_test/
├── files/                          # Archivos de datos de entrada
│   ├── prueba.xlsx                 # 30,000 simulaciones de retornos (55 activos)
│   ├── withdrawals.xlsx            # 128 solicitudes de retiro (4 tablas)
│   └── Insights - Prueba ... .pdf  # Enunciado original de la evaluación
│
├── exercise1-datamanagement/       # Ejercicio 1: Gestión de Datos
│   └── querys.md
│
├── exercise2-portafolio/           # Ejercicio 2: Análisis de Portafolio
│   └── analysis.ipynb
│
├── exercise3-automatization/       # Ejercicio 3: Automatización
│   ├── withdrawals.ipynb
│   ├── decisions_db.csv            # Output: 128 decisiones
│   └── review_hold.csv             # Output: 35 casos en revisión
│
└── exercise4-agentsolution/        # Ejercicio 4: Agente con IA
    ├── 01-investigation.md
    ├── 02-design.md
    ├── 03-system-prompt.md
    ├── 05-demo.md
    ├── agent.py
    ├── memory.json
    ├── prompts.md
    ├── outputs.md
    └── transcripcion.txt
```

---

## Ejercicios

### Ejercicio 1 — Gestión de Datos

**Archivo:** [exercise1-datamanagement/querys.md](exercise1-datamanagement/querys.md)

Diseño de consultas usando un DSL personalizado (operaciones `filter()`, `join()`, `drop()`) sobre cuatro tablas relacionales: `USUARIOS`, `PORTAFOLIOS`, `ASESORES` y `BALANCES`.

El objetivo es obtener los balances de portafolio de usuarios gestionados por un asesor específico, filtrados por fecha y tipo de portafolio. Incluye equivalencia en SQL y recomendación de MongoDB Scheduled Triggers para automatización.

---

### Ejercicio 2 — Análisis de Portafolio

**Archivo:** [exercise2-portafolio/analysis.ipynb](exercise2-portafolio/analysis.ipynb)

Análisis cuantitativo de dos portafolios usando 30,000 simulaciones de Monte Carlo:

| Portafolio | Retorno Esperado | Volatilidad |
|------------|-----------------|-------------|
| P1         | 9.12%           | 20.62%      |
| P2         | 5.84%           | 10.11%      |

Incluye comparación de modelos de IA (Claude vs. Gemini) para análisis del impacto de un alza de tasas de la Fed sobre portafolios de renta fija y variable.

**Tecnologías:** Python, NumPy, Pandas, Jupyter, OpenPyXL

---

### Ejercicio 3 — Automatización de Retiros

**Archivo:** [exercise3-automatization/withdrawals.ipynb](exercise3-automatization/withdrawals.ipynb)

Motor de decisiones automáticas para aprobar, rechazar o poner en revisión solicitudes de retiro. Procesa 128 solicitudes aplicando 9 códigos de razón con tres niveles de severidad.

| Decisión | Casos | Criterios principales |
|----------|-------|-----------------------|
| APPROVE  | 51    | Cuenta activa, KYC verificado, fondos suficientes |
| REJECT   | 42    | Cuenta inactiva, KYC fallido, monto inválido, AML alto |
| HOLD     | 35    | Fondos insuficientes, destino modificado recientemente, AML medio |

**Outputs:** `decisions_db.csv` (todas las decisiones) y `review_hold.csv` (casos HOLD ordenados por severidad).

Incluye propuesta de arquitectura escalable con RabbitMQ, Redis, Claude API y MongoDB.

**Tecnologías:** Python, Pandas, datetime, Jupyter

---

### Ejercicio 4 — Agente Conversacional con IA

**Archivos principales:**
- [exercise4-agentsolution/agent.py](exercise4-agentsolution/agent.py) — Implementación del agente (397 líneas)
- [exercise4-agentsolution/01-investigation.md](exercise4-agentsolution/01-investigation.md) — Investigación sobre ACH
- [exercise4-agentsolution/02-design.md](exercise4-agentsolution/02-design.md) — Arquitectura y flujo
- [exercise4-agentsolution/03-system-prompt.md](exercise4-agentsolution/03-system-prompt.md) — System prompt completo
- [exercise4-agentsolution/05-demo.md](exercise4-agentsolution/05-demo.md) — Demos y reflexión

Agente conversacional para guiar a clientes en el proceso de fondeo de cuentas vía ACH (transferencia bancaria). El agente sigue un flujo estricto de 7 preguntas, infiere el número de ruta bancaria a partir del banco y estado del cliente, valida montos ($1–$25,000) y maneja errores NACHA (R01, R03, R10).

**Características principales:**
- Memoria de sesión persistente en `memory.json`
- Registro de conversaciones en `transcripcion.txt`
- Validación de montos, número de cuenta y tipo de cuenta por regex
- Detección de errores bancarios en lenguaje natural
- Separación clara entre lógica de validación (Python) y conversación (LLM)

**Tecnologías:** Python, Google Gemini API (`gemini-2.5-flash-lite`), dotenv, JSON, Regex

---

## Requisitos

```bash
pip install pandas numpy openpyxl jupyter google-generativeai python-dotenv
```

Para el agente (Ejercicio 4), crear un archivo `.env` con:

```
GEMINI_API_KEY=tu_clave_aqui
```

---

## Uso del Agente (Ejercicio 4)

```bash
cd exercise4-agentsolution
python agent.py
```

El agente iniciará una sesión interactiva. Para reiniciar la sesión, escribe `reset`.

---

## Tecnologías Utilizadas

| Tecnología | Ejercicios |
|------------|-----------|
| Python | 2, 3, 4 |
| Jupyter Notebooks | 2, 3 |
| Pandas / NumPy | 2, 3 |
| Google Gemini API | 4 |
| SQL / DSL personalizado | 1 |
| JSON / Regex | 4 |

---

## Autor

Prueba realizada para **Insights Wealth Management** — Marzo 2026.
