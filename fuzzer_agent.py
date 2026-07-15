import os
import requests
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# 1. Definimos el Estado que viajará a través del agente
class AgentState(TypedDict):
    swagger_url: str
    target_base_url: str
    endpoints_found: List[str]
    attack_plan: str
    security_report: str

# Inicializamos el LLM (puedes usar GPT-4o, Claude 3.5 Sonnet, etc.)
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

# 2. NODO 1: Analizar el contrato OpenAPI
def analyze_swagger(state: AgentState) -> AgentState:
    print("[Agent] Descargando y analizando OpenAPI de Spring Boot...")
    try:
        response = requests.get(state["swagger_url"])
        swagger_data = response.json()
        paths = list(swagger_data.get("paths", {})\
.keys())
    except Exception as e:
        paths = [f"Error al conectar: {str(e)}"]

    # Pedimos al LLM que elabore una estrategia de ataque basada en las rutas encontradas
    prompt = f"Actúa como un Pentester senior. Analiza estas rutas de un microservicio Spring Boot: {paths}. Diseña un plan de pruebas para intentar saltarte la seguridad o corromper los inputs de datos."
    
    ai_response = llm.invoke([SystemMessage(content=prompt)])
    
    return {
        **state,
        "endpoints_found": paths,
        "attack_plan": ai_response.content
    }

# 3. NODO 2: Ejecutar los ataques (Fuzzing) simulados o reales
def execute_fuzzing(state: AgentState) -> AgentState:
    print("[Agent] Ejecutando plan de auditoría...")
    # Aquí es donde el LLM, usando el plan anterior, generaría las peticiones.
    # Para este MVP, le pediremos que redacte el reporte final consolidando los puntos débiles.
    prompt = f"Basándote en el plan de ataque: {state['attack_plan']}, genera un reporte final en Markdown detallando qué endpoints deberíamos monitorizar más de cerca en Spring Boot y qué inputs validar."
    
    ai_response = llm.invoke([SystemMessage(content=prompt)])
    
    return {
        **state,
        "security_report": ai_response.content
    }

# 4. Construcción del Flujo (Grafo de LangGraph)
workflow = StateGraph(AgentState)

# Añadimos los nodos
workflow.add_node("analyzer", analyze_swagger)
workflow.add_node("fuzzer", execute_fuzzing)

# Conectamos los nodos (Flujo secuencial simple para empezar)
workflow.add_edge(START, "analyzer")
workflow.add_edge("analyzer", "fuzzer")
workflow.add_edge("fuzzer", END)

# Compilamos el agente
security_agent = workflow.compile()

# --- EJECUCIÓN ---
if __name__ == "__main__":
    # Asegúrate de tener tu SPRING BOOT corriendo localmente antes de ejecutar esto
    # Por defecto, Springdoc expone el JSON en: http://localhost:8080/v3/api-docs
    
    inputs = {
        "swagger_url": "http://localhost:8080/v3/api-docs",
        "target_base_url": "http://localhost:8080",
        "endpoints_found": [],
        "attack_plan": "",
        "security_report": ""
    }
    
    print("Iniciando Agente de Seguridad Satélite...")
    final_state = security_agent.invoke(inputs)
    
    print("\n" + "="*40)
    print(" REPORTE DE SEGURIDAD GENERADO POR EL AGENTE")
    print("="*40)
    print(final_state["security_report"])