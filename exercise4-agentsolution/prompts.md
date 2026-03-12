# Prompts utilizados — Ejercicio 4
**Modelo utilizado:** Claude (Anthropic) — claude.ai

---

## 4.1.1 ¿Cómo funciona ACH en EE.UU.?

**Prompt:**
> "explícame cómo funciona ACH en EE.UU., el flujo completo desde el originador hasta el receptor, tiempos de liquidación para ACH estándar vs Same-Day ACH, y cuándo recomendarías Same-Day a un cliente de Insights"

---

## 4.1.2 Requisitos para fondear una cuenta vía ACH

**Prompt:**
> "qué información necesita un usuario para configurar un ACH pull? incluyendo datos bancarios, proceso de verificación, límites típicos, tiempos de disponibilidad y 3 razones comunes de rechazo con su código Nacha"

---

## 4.1.3 Routing numbers ABA

**Prompt:**
> "qué es un ABA routing number, cuál es su estructura, y por qué un banco puede tener routing distintos por estado? dame una tabla con bancos comunes para latinos en EE.UU. con sus routing numbers por estado"

---

## 4.1.4 Comparativa ACH vs Wire vs Debit Card

**Prompt:**
> "construye una tabla comparativa entre ACH, Wire Transfer y Debit Card según velocidad, costo, límites, reversibilidad y experiencia de usuario. por qué ACH sería el preferido para Insights?"

---

## 4.2 Diseño del agente

**Prompt:**
> "ayúdame a diseñar el flujo conversacional de un agente que atiende clientes que quieren fondear su cuenta vía ACH. debe preguntar banco y estado antes de dar cualquier información"

---

## 4.3 System prompt

**Prompt:**
> "escribe el system prompt completo para un agente ACH de Insights. debe incluir rol y tono, flujo de preguntas en orden, lógica para inferir routing, manejo de fallos R01 R03 R10 y disclaimer"

---

## 4.4 Implementación

**Prompt:**
> "construye un agente en Python usando la API de Gemini que guíe a clientes para fondear su cuenta vía ACH, con lookup de routing numbers, manejo de errores Nacha y memoria entre sesiones"