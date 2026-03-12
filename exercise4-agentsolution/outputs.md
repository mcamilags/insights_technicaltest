# Outputs del modelo — Ejercicio 4
**Modelo utilizado:** Claude (Anthropic) — claude.ai

---

## 4.1.1 Output — ¿Cómo funciona ACH en EE.UU.?

ACH (Automated Clearing House) es la red que mueve dinero entre cuentas bancarias en EE.UU. El flujo completo es:

**Originator → ODFI → ACH Network → RDFI → Receiver**

- **Originator:** el cliente que inicia la transacción
- **ODFI:** Insights, quien origina la instrucción en la red
- **ACH Network:** la autopista que conecta todos los bancos, procesa en lotes varias veces al día
- **RDFI:** el banco del cliente, quien recibe la instrucción y suelta los fondos
- **Receiver:** la cuenta destino en Insights

**Tiempos:** ACH estándar tarda 1-3 días hábiles. Same-Day ACH llega el mismo día si se envía antes de las 2:45pm ET.

**¿Cuándo Same-Day?** Cuando el cliente quiere aprovechar una oportunidad de mercado ese mismo día — el costo adicional vale la pena en ese contexto.

---

## 4.1.2 Output — Requisitos para fondear vía ACH

**Datos requeridos:** nombre del titular, routing number (ABA), número de cuenta, tipo de cuenta (checking/savings).

**Verificación:** micro-depósitos (1-2 días) o verificación instantánea vía Plaid.

**Límites típicos:** $25,000 por transacción, $50,000 diario, $100,000 mensual.

**Códigos Nacha:**
- R01: fondos insuficientes
- R03: cuenta inválida o inexistente  
- R10: débito no autorizado por el titular

---

## 4.1.3 Output — Routing numbers ABA

Un ABA routing number es un código de 9 dígitos que identifica bancos en la red de pagos de EE.UU. Estructura:
- Primeros 4 dígitos: distrito de la Reserva Federal
- Dígitos 5-8: identificador de la institución
- Dígito 9: dígito verificador

Los bancos grandes tienen routing distintos por estado porque heredaron los números de los bancos regionales que compraron al expandirse. Cada región mantiene su propio centro de procesamiento ACH.

**Tabla de routing numbers verificados:**

| Banco | Estado | Routing |
|-------|--------|---------|
| Bank of America | Texas | 111000025 |
| Bank of America | California | 121000358 |
| Bank of America | Florida | 063100277 |
| Chase | Texas | 111000614 |
| Chase | California | 322271627 |
| Chase | Florida | 267084131 |
| Wells Fargo | Texas | 111900659 |
| Wells Fargo | California | 121042882 |
| Citibank | Texas | 113193532 |
| Citibank | New York | 021000089 |
| TD Bank | Florida | 067014822 |
| TD Bank | New York | 026013673 |

---

## 4.1.4 Output — Comparativa ACH vs Wire vs Debit Card

| Criterio | ACH | Wire | Debit Card |
|----------|-----|------|------------|
| Velocidad | 1-3 días | Mismo día | Inmediato |
| Costo | Gratis o muy bajo | $15-$50 | 1-3% |
| Límites | $25,000 | Sin límite | $2,000-$5,000 |
| Reversible | Sí (60 días) | No | Sí |
| UX | Routing + cuenta | Datos completos | Solo tarjeta |

ACH es el preferido para Insights porque combina bajo costo con límites adecuados para inversiones. Wire se recomienda para montos grandes y urgentes. Debit Card para depósitos pequeños e inmediatos.