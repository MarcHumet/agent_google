Cómo configurarlo en tu sistema Pop!_OS usando uv para que gestionarlo en el mismo entorno de trabajo y que sea ultra rápido:

1. Instalación del ADK

Para tener acceso al comando adk, primero debes instalar la librería oficial. Con uv es muy sencillo:
```Bash

uv add google-adk
uv add google-genai
```
(Esto instalará el binario globalmente en tu sistema para que puedas usar el comando adk en cualquier carpeta).
2. Configurar la API Key

Como ya tienes la variable $GOOGLE_API_KEY, asegúrate de que esté en tu archivo .bashrc o .zshrc para que sea permanente, o expórtala en la sesión actual:
```Bash

export GOOGLE_API_KEY="tu_llave_aqui"
```
3. Crear tu Agente (El comando que buscabas)
En la carpeta src generar el argivo agent.py

```Python


from google.adk import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search 

root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(model="gemini-2.5-flash-lite-preview-09-2025"),  # Tu modelo correcto  # ✅ 15 RPM gratis
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info.",
    tools=[google_search],
)
logger.debug("✅ Root Agent defined.") 

# No Funcionan
# ✅ gemini-2.0-flash-lite-001
# ✅ gemini-2.0-flash-lite
# ✅ gemini-2.0-flash-lite-preview-02-05
# ✅ gemini-2.0-flash-lite-preview


#Modelos testeados que funcionan con ASK modalidad gratuita:

# ✅ gemini-flash-lite-latest
# ✅ gemini-2.5-flash-lite
# ✅ gemini-2.5-flash
# ✅ gemini-2.5-flash-lite-preview-09-2025
```

 linux, ir a la carpetaque contiene el archivo agent.yaml
Ahora puedes ejecutar el comando de creación. El ADK generará una carpeta con la estructura necesaria (archivos de configuración, prompts y el punto de entrada de Python):
```Bash

uv run adk web --reload_agents --port 8082
```
¿Qué contiene esa carpeta?

    agent.yaml: Configuración del modelo y herramientas (tools).

    main.py: El código Python donde puedes añadir lógica personalizada.

    prompts/: Carpeta para las instrucciones del sistema.

4. Ejecutar la Interfaz Web del ADK

Una de las mejores funciones del ADK es que incluye una interfaz de pruebas local (el "Web Interface" que mencionabas antes). Una vez creado el agente, entra en la carpeta y lánzalo:
```Python

# agent.py (guarda en ~/project/agents/agent_google/agent.py)

from google.adk import Agent, google_search
from google.adk.models.google_llm import Gemini

root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(model="gemini-2.0-flash-exp"),  # Tu modelo correcto
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info.",
    tools=[google_search],
)

```
Esto abrirá automáticamente una pestaña en tu navegador (normalmente en localhost:8080) donde podrás hablar con el agente, ver los logs de las herramientas y testear la visión multimodal de Gemini 2.5 Flash-lite.
Si el comando !adk lo viste en un Notebook (Colab):

Si estás intentando replicar esto en VS Code (en tus celdas interactivas), no pongas el signo !. En tu terminal de Pop!_OS o en la celda de VS Code, usa simplemente:
```Python

# En una celda de VS Code
import os
os.environ["GOOGLE_API_KEY"] = "tu_key"

# Para ejecutar comandos de sistema desde la celda usa % (magics)
%pip install google-agent-sdk
```
