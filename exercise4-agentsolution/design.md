## 4.2 Diseño del agente (arquitectura y flujo conversacional)

### Propósito

El agente tiene como objetivo automatizar la atención a clientes que desean depositar dinero en su cuenta de inversiones vía ACH, guiándolos paso a paso desde la recopilación de datos hasta la confirmación del depósito.

---

### Regla obligatoria

El agente debe preguntar banco y estado antes de dar cualquier información, porque el routing number depende de ambos. Sin esos dos datos no es posible darle al cliente la información correcta para su transferencia.

---

### Flujo conversacional

#### Estados del agente

```
1. RECOPILACIÓN DE DATOS
2. INFERENCIA DE ROUTING
3. INSTRUCCIONES
4. CONFIRMACIÓN
5. MANEJO DE FALLOS
```

#### Preguntas en orden

| # | Pregunta | ¿Qué hace el agente con la respuesta? |
|---|----------|--------------------------------------|
| 1 | ¿En qué banco tienes tu cuenta? | Guarda el banco para el lookup |
| 2 | ¿En qué estado abriste esa cuenta? | Guarda el estado para el lookup |
| — | *(inferencia automática)* | Busca routing en tabla banco + estado |
| 3 | ¿Cuánto quieres depositar? | Valida que el monto sea > 0 y ≤ límite |
| 4 | ¿Lo necesitas estándar (1–3 días) o urgente (mismo día)? | Determina tipo de ACH |
| 5 | ¿Cuál es tu número de cuenta? | Guarda para instrucciones finales |
| 6 | ¿Es cuenta checking o savings? | Completa los datos necesarios |

---

### Transiciones entre estados

**Recopilación → Inferencia de routing**
Cuando el agente tiene banco y estado, busca automáticamente en su tabla interna y le muestra el routing al cliente para confirmación. Si el cliente no lo reconoce, le pide que lo verifique en su app bancaria.

**Inferencia → Instrucciones**
Con todos los datos completos, el agente le da al cliente las instrucciones paso a paso para completar el depósito desde su banco.

**Instrucciones → Confirmación**
El agente le pregunta al cliente si logró completar el proceso y confirma que todo quedó en orden.

**Cualquier estado → Manejo de fallos**
Si el proceso falla, el agente identifica el código de error y responde así:

| Código | Mensaje al cliente |
|--------|-------------------|
| **R01** | *"No tienes fondos suficientes en tu cuenta para completar esta transferencia. Por favor verifica tu saldo e intenta de nuevo."* |
| **R03** | *"No encontramos una cuenta activa con los datos que ingresaste. Por favor revisa tu número de cuenta y routing number."* |
| **R10** | *"La transacción no fue autorizada por tu banco. Por favor contáctanos para verificar tu información."* |
