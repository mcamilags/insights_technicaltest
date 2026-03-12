## 4.1 Investigación previa

---

### 4.1.1 ¿Cómo funciona ACH en EE.UU.?

ACH (Automated Clearing House) es la red que mueve dinero entre cuentas bancarias en EE.UU. Cuando un cliente quiere fondear su cuenta, le pasa el dinero a una entidad, en este caso Insights inicia la transacción. Luego el dinero viaja a través de la red ACH hasta el banco del cliente, que tiene la plata y la manda a Insights para que los fondos queden disponibles en la cuenta.

El flujo completo es: **Originator → ODFI → ACH Network → RDFI → Receiver**, donde Insights actúa como ODFI (quien origina la transacción) y el banco del cliente como RDFI (quien recibe la instrucción y suelta los fondos).

#### Tiempos de liquidación

- **ACH Estándar** puede tardar de 1-3 días
- **Same-Day ACH** es el mismo día.

#### ¿Cuándo recomendar Same-Day a un cliente de Insights?

Cuando hay una oportunidad de mercado que el cliente quiere aprovechar ese mismo día, por ejemplo, si algo está a punto de llegar a su fecha de cierre, lo mejor sería usar Same-Day. En ese contexto, el costo adicional valdría la pena. 
Aunque ACH estándar es suficiente y más eficiente para depósitos de rutina.

---

### 4.1.2 Requisitos para fondear una cuenta de inversión vía ACH

Para configurar un ACH pull, el cliente necesita proveer:

| Campo | Descripción |
|-------|-------------|
| **Nombre del titular** | Debe coincidir exactamente con el nombre registrado en el banco |
| **Routing number (ABA)** | 9 dígitos: identifica el banco en la red de pagos |
| **Account number** | Identifica la cuenta específica del cliente |
| **Tipo de cuenta** | Checking o Savings |

#### Proceso de verificación

Antes del primer depósito, Insights verifica que la cuenta le pertenece al cliente mediante micro-depósitos (dos depósitos pequeños que el cliente debe confirmar, tarda 1–2 días) o verificación instantánea vía Plaid.

#### Límites típicos

| Tipo | Límite |
|------|--------|
| Por transacción | $25,000 |
| Diario | $50,000 |
| Mensual | $100,000 |

#### Códigos de rechazo Nacha más comunes

| Código | En simple | Mensaje al cliente |
|--------|-----------|-------------------|
| **R01** | Fondos insuficientes | *"Tu cuenta no tiene saldo suficiente para completar esta transferencia. Verifica tu saldo e intenta de nuevo."* |
| **R03** | La cuenta no existe | *"No encontramos una cuenta activa con los datos que ingresaste. Verifica tu número de cuenta y routing number."* |
| **R10** | El débito no fue autorizado por el titular | *"Tu banco reportó que esta transacción no fue autorizada. Contáctanos para verificar tu información."* |

---

### 4.1.3 Routing Numbers (ABA): lógica y lookup por banco y estado

Un ABA routing number es un código de 9 dígitos que identifica a los bancos en la red de pagos de EE.UU. Los primeros 4 dígitos indican en cuál de los 12 distritos de la Reserva Federal opera el banco.

Los grandes bancos tienen routing numbers distintos por estado porque cuando se expandieron nacionalmente, heredaron los routing numbers de cada banco regional que compraron. Los mantienen separados porque cada región tiene su propio centro de procesamiento ACH.

#### Tabla de routing numbers — Bancos comunes (enfoque latinos en EE.UU.)

| Banco | Estado | Routing Number | Fuente |
|-------|--------|---------------|--------|
| **Bank of America** | Texas | 111000025 | [onlinebankinghelp.com](https://www.onlinebankinghelp.com/routing-numbers/bank-of-america/) |
| **Bank of America** | California | 121000358 | [onlinebankinghelp.com](https://www.onlinebankinghelp.com/routing-numbers/bank-of-america/) |
| **Bank of America** | Florida | 063100277 | [onlinebankinghelp.com](https://www.onlinebankinghelp.com/routing-numbers/bank-of-america/) |
| **Chase** | Texas | 111000614 | [onlinebankinghelp.com](https://www.onlinebankinghelp.com/routing-numbers/chase/) |
| **Chase** | California | 322271627 | [onlinebankinghelp.com](https://www.onlinebankinghelp.com/routing-numbers/chase/) |
| **Chase** | Florida | 267084131 | [onlinebankinghelp.com](https://www.onlinebankinghelp.com/routing-numbers/chase/) |
| **Wells Fargo** | Texas | 111900659 | [muralpay.com](https://muralpay.com/blog/wells-fargo-routing-numbers-in-the-us-complete-list) |
| **Wells Fargo** | California | 121042882 | [muralpay.com](https://muralpay.com/blog/wells-fargo-routing-numbers-in-the-us-complete-list) |
| **Citibank** | Texas | 113193532 | [gobankingrates.com](https://www.gobankingrates.com/banking/banks/citibank-routing-number/) |
| **Citibank** | New York | 021000089 | [gobankingrates.com](https://www.gobankingrates.com/banking/banks/citibank-routing-number/) |
| **Citibank** | Florida | 266086554 | [gobankingrates.com](https://www.gobankingrates.com/banking/banks/citibank-routing-number/) |
| **TD Bank** | Florida | 067014822 | [gobankingrates.com](https://www.gobankingrates.com/banking/banks/how-find-td-bank-routing-number/) |
| **TD Bank** | New York (metro) | 026013673 | [gobankingrates.com](https://www.gobankingrates.com/banking/banks/how-find-td-bank-routing-number/) |
| **TD Bank** | New Jersey | 031201360 | [gobankingrates.com](https://www.gobankingrates.com/banking/banks/how-find-td-bank-routing-number/) |

> Los routing numbers pueden cambiar. Siempre verificar con el banco antes de usar.

#### ¿Cómo decide el agente el routing correcto?

Cuando el cliente dice *"Bank of America en Texas"*, el agente busca en su tabla interna banco + estado, encuentra el routing correspondiente y se lo muestra al cliente para confirmación. Si el cliente no lo reconoce, el agente le pide que lo verifique en su app bancaria, por lo que el cliente no necesita saber su routing de memoria.

---

### 4.1.4 Comparativa: ACH vs Wire vs Debit Card

| Criterio | ACH | Wire Transfer | Debit Card |
|----------|-----|--------------|------------|
| **Velocidad** | 1–3 días (Same-Day disponible) | Mismo día | Instantáneo |
| **Costo** | Gratuito o muy bajo | $15–$50 | 1–3% comisión |
| **Límites** | Hasta $25,000 por transacción | Sin límite práctico | $2,000–$5,000 diario |
| **Reversibilidad** | Sí (hasta 60 días) | No | Sí (chargeback) |
| **Experiencia usuario** | Routing + account number | Datos bancarios completos | Solo número de tarjeta |

#### ¿Por qué ACH es el método preferido para Insights?

ACH combina bajo costo con los límites adecuados para inversiones, lo cual es ideal para un cliente activo que deposita regularmente. El costo casi nulo lo hace escalable para miles de clientes sin afectar márgenes.

#### ¿Cuándo recomendar Wire o Debit Card?

- **Wire** -> cuando el cliente necesita mover mucha plata de manera urgente y el monto supera los límites de ACH.
- **Debit Card** -> para depósitos más pequeños donde el cliente quiere disponibilidad inmediata.
