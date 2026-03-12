# 4.5 Demo y Reflexión — Agente ACH

## Escenarios demostrados

### Escenario 1 — Éxito 

**Descripción:** Cliente nuevo completa un depósito ACH estándar sin inconvenientes.

```
Agente: ¡Hola! Bienvenido a Insights Wealth Management. ¿Con quién tengo el gusto?

Tu: Maria

Agente: ¡Hola María! Con mucho gusto te ayudo a fondear tu cuenta de inversiones.
        ¿En qué banco tienes tu cuenta?

Tu: Chase

Agente: Perfecto. ¿En qué estado abriste esa cuenta de Chase?

Tu: Texas

Agente: El routing number para Chase en Texas es 111000614. ¿Es correcto?

Tu: si

Agente: Recuerda que tus datos están protegidos bajo los estándares de seguridad
        de Insights Wealth Management. Nunca compartiremos tu información con terceros.
        ¿Cuánto deseas depositar? (mínimo $1, máximo $25,000)

Tu: 5000

Agente: Entendido, $5,000.00. ¿Lo necesitas estándar (1-3 días hábiles) o urgente (mismo día)?

Tu: estandar

Agente: ¿Cuál es tu número de cuenta bancaria?

Tu: 1234567890

Agente: ¿Es una cuenta checking o savings?

Tu: checking

Agente: María, aquí está el resumen de tu operación:
        - Banco: Chase | Estado: Texas | Routing: 111000614
        - Cuenta: 1234567890 (Checking)
        - Monto: $5,000.00 | Velocidad: Estándar (1-3 días hábiles)
        ¿Confirmas para proceder?

Tu: si

Agente: ¡Perfecto, María! Tu depósito ha sido iniciado. Te notificaremos cuando se acredite.

Tu: salir

Agente: ¡Hasta luego, María! Fue un placer ayudarte en Insights WM.
[Transcripcion guardada en transcripcion.txt]
```

---

### Escenario 2 — R01: Fondos Insuficientes 

**Descripción:** El banco rechaza la transferencia por fondos insuficientes.

```
Agente: ¡Hola! ¿Con quién tengo el gusto?

Tu: Carlos

Agente: ¡Hola Carlos! ¿En qué banco tienes tu cuenta?

Tu: Bank of America

Agente: ¿En qué estado abriste esa cuenta?

Tu: Florida

Agente: El routing number para Bank of America en Florida es 063100277. ¿Es correcto?

Tu: si

Agente: ¿Cuánto deseas depositar?

Tu: 10000

Agente: ¿Lo necesitas estándar o urgente?

Tu: urgente

Agente: ¿Cuál es tu número de cuenta bancaria?

Tu: 9876543210

Agente: ¿Es checking o savings?

Tu: savings

Agente: Carlos, resumen de tu operación:
        - Banco: Bank of America | Florida | Routing: 063100277
        - Cuenta: 9876543210 (Savings)
        - Monto: $10,000.00 | Urgente (mismo día)
        ¿Confirmas?

Tu: R01

Agente: Fondos insuficientes: tu banco rechazó la transferencia porque no
        había saldo suficiente. Por favor verifica tu saldo e inténtalo de nuevo.

Tu: salir
[Transcripcion guardada en transcripcion.txt]
```

---

### Escenario 3 — R03: Cuenta Inválida 

**Descripción:** El banco rechaza la transferencia porque la cuenta no existe.

```
Agente: ¡Hola! ¿Con quién tengo el gusto?

Tu: Laura

Agente: ¡Hola Laura! ¿En qué banco tienes tu cuenta?

Tu: Wells Fargo

Agente: ¿En qué estado abriste esa cuenta?

Tu: California

Agente: El routing number para Wells Fargo en California es 121042882. ¿Es correcto?

Tu: si

Agente: ¿Cuánto deseas depositar?

Tu: 3000

Agente: ¿Lo necesitas estándar o urgente?

Tu: estandar

Agente: ¿Cuál es tu número de cuenta bancaria?

Tu: 1111111111

Agente: ¿Es checking o savings?

Tu: checking

Agente: Laura, resumen de tu operación:
        - Banco: Wells Fargo | California | Routing: 121042882
        - Cuenta: 1111111111 (Checking)
        - Monto: $3,000.00 | Estándar (1-3 días hábiles)
        ¿Confirmas?

Tu: R03

Agente: Cuenta inválida: no encontramos una cuenta activa con los datos que
        ingresaste. Por favor revisa tu número de cuenta y routing number.

Tu: salir
[Transcripcion guardada en transcripcion.txt]
```
Todo esto se encuentra en transcription.txt

---

## Reflexión (~200 palabras)

Construir este agente fue un ejercicio valioso para entender tanto las capacidades como las limitaciones de los LLMs en flujos financieros estructurados.

Lo que funcionó bien fue la combinación de dos capas: el LLM manejando el lenguaje natural y la conversación, mientras que el código Python se encargó de las validaciones duras: montos, routing numbers, normalización de nombres de banco. Esta separación es clave porque no se puede depender únicamente del modelo para validar datos críticos; un LLM puede alucinar un routing number o aceptar un monto inválido si el prompt no es suficientemente estricto.

Con más tiempo mejoraría varias cosas. Primero, la detección de intención: actualmente el agente sigue un flujo lineal pregunta por pregunta, pero un cliente real podría escribir "quiero depositar $5,000 desde mi Chase en Texas" y el agente debería extraer los cuatro datos de un solo mensaje. Segundo, agregaría autenticación real, en producción el cliente ya estaría logueado y el agente recibiría su perfil desde una API interna, eliminando la necesidad de preguntar banco y estado en cada sesión. Tercero, implementaría reintentos automáticos para R01 con un límite de intentos antes de escalar al equipo humano.

La mayor limitación encontrada fue la cuota del tier gratuito de Gemini, que obligó a ser muy cuidadoso con el número de requests durante las pruebas. En un entorno de producción esto se resuelve con billing y rate limiting apropiado.