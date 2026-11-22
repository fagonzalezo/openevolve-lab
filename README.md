# Laboratorio de OpenEvolve (con asistente de programación)

> Este laboratorio está basado en el repositorio original [`rramosp/openevolve-lab`](https://github.com/rramosp/openevolve-lab), del cual este repositorio es un *fork*.

Un laboratorio práctico para explorar la búsqueda evolutiva guiada por LLMs con **OpenEvolve** (una implementación de código abierto de AlphaEvolve de DeepMind). Aprenderás cómo MAP-Elites, las poblaciones en islas y la retroalimentación del evaluador trabajan en conjunto para evolucionar código y prompts de forma automática en tareas como **minimización de funciones**, **regresión simbólica** y **optimización de prompts**.

También usarás tu asistente de programación para entender y modificar el código.

Te guiaremos para hacer:

- **Regresión simbólica**: descubrir, a partir de los datos, una ecuación para la tasa de crecimiento de una población en función del tiempo $t$ y de la población $P$. Este es uno de los ejemplos del [repositorio original de `openevolve`](https://github.com/algorithmicsuperintelligence/openevolve).

$$\frac{dP}{dt} = f(t, P) \quad \text{¿cuál es } f\text{?}$$

  También explorarás cómo el conocimiento del dominio que tiene el LLM influye en la búsqueda: ¿lo ayuda a encontrar la ecuación correcta o lo sesga hacia los modelos de los libros de texto?

![regresión simbólica](imgs/symreg.png)

- **Optimización de prompts**: resolver la clasificación de tickets de soporte al cliente con un prompt optimizado.

![optimización de prompts](imgs/promptopt.png)

---

## 1. Configuración e instalación

### 1.1 Configura y verifica tu API key del LLM

Por defecto, en este laboratorio usaremos la **API de Google Gemini**, que ofrece un nivel gratuito suficiente para el taller. Te recomendamos usar tu **cuenta personal de Google** (no la institucional), ya que las cuentas institucionales a menudo tienen restringido el acceso a Google AI Studio.

**Cómo generar una API key en Google AI Studio:**

1. Ingresa a [Google AI Studio](https://aistudio.google.com/) e inicia sesión con tu cuenta personal de Google.
2. Acepta los términos de uso si es la primera vez que ingresas.
3. Ve a la sección **Get API key** (o directamente a [aistudio.google.com/apikey](https://aistudio.google.com/apikey)).
4. Haz clic en **Create API key**. Si te lo pide, selecciona o crea un proyecto de Google Cloud.
5. Copia la clave generada y guárdala en un lugar seguro. **No la compartas ni la subas a ningún repositorio.**

Verifica que tu API key funciona usando [`call_model.py`](./call_model.py):

- **Opción A (por defecto) — Usando Google Gemini:**
  ```bash
  export OPENAI_COMPATIBLE_API_KEY="tu-api-key-de-gemini"
  export OPENAI_COMPATIBLE_URL="https://generativelanguage.googleapis.com/v1beta/openai"
  export MODEL="gemini-3.5-flash"
  python call_model.py "cuál es el sentido de la vida"
  ```

- **Opción B — Usando OpenRouter:** también puedes usar cualquier otro LLM compatible con la API de OpenAI. Por ejemplo, puedes obtener una clave gratuita para uso limitado en [OpenRouter](https://openrouter.ai/) (el modelo `openrouter/free` agrupa varios modelos gratuitos).
  ```bash
  export OPENAI_COMPATIBLE_API_KEY="tu-api-key-de-openrouter"
  export OPENAI_COMPATIBLE_URL="https://openrouter.ai/api/v1"
  export MODEL="openrouter/free"
  python call_model.py "cuál es el sentido de la vida"
  ```

### 1.2 Clona, instala y configura `openevolve`

Clona el repositorio de `openevolve`:

```bash
git clone https://github.com/algorithmicsuperintelligence/openevolve.git
cd openevolve
```

Instala las dependencias con [`uv`](https://docs.astral.sh/uv/) (si no lo tienes, sigue las [instrucciones de instalación](https://docs.astral.sh/uv/getting-started/installation/)). Este comando crea un entorno virtual en la carpeta `.venv` e instala `openevolve` y sus dependencias:

```bash
uv sync
```

Activa el entorno virtual:

- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\activate
  ```

Recuerda activar el entorno virtual cada vez que abras una nueva terminal para trabajar en el laboratorio.

Luego edita `examples/function_minimization/config.yaml` y configura los modelos, ya que los que vienen en el archivo original están obsoletos:

```yaml
llm:
  primary_model: "gemini-3.5-flash-lite"
  secondary_model: "gemini-3.5-flash"
```

El parámetro `api_base` solo debe cambiarse si usas una API key distinta a la de Gemini (por ejemplo, OpenRouter). En ese caso, ajusta `primary_model`, `secondary_model` y `api_base` a los mismos valores que usaste en las variables `$MODEL` y `$OPENAI_COMPATIBLE_URL`.

### 1.3 Ejecuta tu primera evolución y visualiza los resultados

Ejecuta una evolución corta de 5 iteraciones sobre el ejemplo de minimización de funciones (ten en cuenta que `openevolve` lee la variable `$OPENAI_API_KEY`):

```bash
export OPENAI_API_KEY=${OPENAI_COMPATIBLE_API_KEY}
python openevolve-run.py examples/function_minimization/initial_program.py \
         examples/function_minimization/evaluator.py \
         --config examples/function_minimization/config.yaml \
         --iterations 5
```

Inspecciona la carpeta de salida generada:

```bash
ls -R examples/function_minimization/openevolve_output/
```

Lanza el visualizador interactivo de resultados:

```bash
python scripts/visualizer.py
```

---

## 2. Entiende cómo funciona `openevolve`

Abre tu asistente de programación con IA favorito en este repositorio y pregúntale sobre la arquitectura de `openevolve`. Te sugerimos usar [OpenCode](https://opencode.ai/), un asistente de programación de código abierto que funciona en la terminal y se puede configurar con distintos proveedores de LLM, incluido Gemini.

Por ejemplo, intenta preguntarle:

- *"Inspecciona el código en `openevolve` y dame una visión general de cómo funciona OpenEvolve."*
- *"Explica en detalle qué ocurre en cada paso de una iteración."*
- *"Cuando OpenEvolve comienza solo con mi programa inicial, ¿cómo inicializa las islas?"*
- *"¿Cómo garantiza que los programas hijos en diferentes islas se mantengan diversos?"*
- *"Explica en detalle cómo ocurre la mutación del código."*
- *"Dame un ejemplo de un prompt de mutación completo."*
- *"Explica la diferencia entre los modelos primario y secundario en una configuración de OpenEvolve."*

En el [registro de conversación](conversation.md) se encuentra la sesión completa de preguntas y respuestas que el autor del laboratorio original tuvo con Antigravity/Jetski usando Google Gemini.

> **Consejo:** antes de empezar, puedes pedirle a tu asistente de programación que guarde una transcripción de tu sesión:
> *"De ahora en adelante, guarda cada turno de esta conversación en un archivo llamado `conversation.md`, incluyendo las preguntas que hago y las respuestas que me das."*

---

## 3. Entiende la ejecución de ejemplo

Inspecciona los archivos en `openevolve/examples/function_minimization/`:

1. **Entradas (lo que configuras antes de ejecutar `openevolve`)**:
   - `initial_program.py`: el programa base inicial, con los marcadores `# EVOLVE-BLOCK-START ... # EVOLVE-BLOCK-END`.
   - `config.yaml`: el ensamble de LLMs, la base de datos de islas, la grilla de MAP-Elites y la configuración del evaluador.
   - `evaluator.py`: la función de puntuación determinista que califica los programas candidatos.
2. **Salidas (lo que produce `openevolve`)**:
   - Explora `openevolve_output/` para entender cómo se organizan los *checkpoints*, los mejores programas y los metadatos.

Puedes usar `jq` para visualizar de forma legible cualquier archivo JSON:

```bash
jq . metadata.json
jq . best_program_info.json
```

O pídele a tu asistente de programación que analice la ejecución:

- *"Con base en `openevolve/examples/function_minimization/openevolve_output/`, por favor resume los resultados de la ejecución."*
- *"¿Cuántos tokens se usaron en cada iteración?"*

> **Nota:** OpenEvolve puede **no** registrar correctamente el conteo de tokens (ver la sección 4), así que tu asistente podría hacer una suposición sin fundamento en esa última pregunta. Observa si tu asistente de programación detecta este hecho y cómo lo maneja. En la [conversación del laboratorio original](conversation.md) puedes ver cómo lo manejó Antigravity/Jetski.

---

## 4. Modifica `openevolve` para registrar el uso de tokens

Sin un registro del uso de tokens es difícil estimar los costos a partir de una ejecución inicial pequeña. Este problema se presenta en **macOS y Windows**, pero puede no aparecer en **Linux** (los procesos de trabajo de `openevolve` se crean de forma distinta según el sistema operativo).

Por eso, **primero verifica si OpenEvolve está registrando bien los tokens** en tu máquina: revisa los logs de la ejecución anterior (en `examples/function_minimization/openevolve_output/logs/`) y busca mensajes como `LLM Token Usage (...)` con valores de `prompt_tokens`, `completion_tokens` y `total_tokens` para cada llamada al LLM.

Si los tokens no se registran (o se registran de forma incompleta), modifica `openevolve` para que registre el conteo de tokens del prompt y de la respuesta en cada llamada al LLM. Puedes pedirle a tu asistente de programación:

- *"Modifica `openevolve` para que registre los tokens usados en cada llamada al LLM."*

Luego vuelve a ejecutar `openevolve` por 10 iteraciones:

```bash
python openevolve-run.py examples/function_minimization/initial_program.py \
         examples/function_minimization/evaluator.py \
         --config examples/function_minimization/config.yaml \
         --iterations 10
```

Ahora pregúntale de nuevo a tu asistente de programación:

- *"Resume los resultados de la ejecución e incluye un análisis del uso de tokens para que pueda estimar el costo por iteración."*

---

## 5. Ejemplos prácticos

### Opción A: Regresión simbólica

En la carpeta [`example_symbolic_regression/problems/`](example_symbolic_regression/problems) de este repositorio encontrarás problemas de **regresión simbólica** (descubrir una fórmula matemática que se ajuste a un conjunto de puntos) listos para ejecutar. Provienen del ejemplo [`examples/symbolic_regression`](https://github.com/algorithmicsuperintelligence/openevolve/tree/main/examples/symbolic_regression) del repositorio original de `openevolve`, que genera los problemas a partir del benchmark LLM-SRBench. Cada carpeta ya incluye los datos (`*.npy`), el programa inicial, el evaluador y un `config.yaml` configurado con los modelos de Gemini, así que no necesitas generarlos ni descargar nada de Hugging Face.

| Problema | Descripción |
|---|---|
| [`bio_pop_growth/BPG8`](example_symbolic_regression/problems/bio_pop_growth/BPG8) | Tasa de crecimiento de una población `dP_dt` en función del tiempo `t` y la población `P`. El prompt le dice al LLM qué significa cada variable. |
| [`anonymized/BPG8_anon`](example_symbolic_regression/problems/anonymized/BPG8_anon) | **El mismo problema BPG8** (mismos datos, evaluador y configuración), pero sin ninguna pista sobre el dominio: las variables se llaman `x0`, `x1` y `y`, tanto en el mensaje del sistema como en el programa inicial. |
| [`matsci/MatSci18`](example_symbolic_regression/problems/matsci/MatSci18) | Un problema de ciencia de materiales. |

En todos ellos el programa inicial (un modelo lineal) tiene un desempeño pobre y deja mucho margen para la evolución.

**Requisitos previos** (con el entorno virtual de la sección 1.2 activado):

```bash
uv pip install scipy matplotlib pandas jupyter
```

**Cómo lanzar una ejecución** (desde la carpeta `openevolve`, con el entorno virtual activado; ajusta `LAB` a la ruta donde clonaste este repositorio):

```bash
export LAB=/ruta/a/openevolve-lab
export OPENEVOLVE_CONFIG_BASEDIR=${LAB}/example_symbolic_regression/problems/bio_pop_growth/BPG8
python openevolve-run.py ${OPENEVOLVE_CONFIG_BASEDIR}/initial_program.py \
                        ${OPENEVOLVE_CONFIG_BASEDIR}/evaluator.py \
                        --config ${OPENEVOLVE_CONFIG_BASEDIR}/config.yaml \
                        --iterations 50
```

Los resultados se guardan en `openevolve_output/` dentro de la carpeta del problema. Cada problema ya incluye una carpeta `openevolve_output/` con los resultados de una ejecución de referencia; renómbrala antes de lanzar tu ejecución (por ejemplo, a `openevolve_output_referencia`) para conservarla y poder comparar. Luego usa el notebook [`inspect_symbolic_regresion.ipynb`](./inspect_symbolic_regresion.ipynb) para inspeccionar los resultados (cambia la variable `problem_id` para elegir el problema).

**Experimento sugerido: ¿ayuda o sesga el conocimiento del dominio?**

Ejecuta **las dos versiones de BPG8** (`bio_pop_growth/BPG8` y `anonymized/BPG8_anon`) con el mismo número de iteraciones y compara los resultados. Puedes pedirle a tu asistente de programación que te ayude con el análisis:

- ¿Qué fórmula propone el LLM en las primeras iteraciones de cada versión? Revisa los prompts y las respuestas guardadas en `openevolve_output/checkpoints/checkpoint_*/programs/*.json`. ¿Reconoce el LLM que se trata de un modelo de crecimiento poblacional cuando conoce el nombre de las variables?
- ¿Qué tan diferentes son los puntajes y las fórmulas finales? ¿Cuál es más simple e interpretable? ¿Cuántos parámetros usa cada una?
- ¿La mejora en el puntaje entre iteraciones es real, o se debe al ruido de la optimización de parámetros (BFGS parte de valores aleatorios)?
- El evaluador calcula el puntaje sobre los datos de **entrenamiento**. ¿Cómo se comportan las mejores fórmulas de cada versión en los conjuntos de prueba (`X_test_for_eval.npy`) y fuera de distribución (`X_ood_test_for_eval.npy`)?

Usa tu asistente de programación para depurar cualquier problema que encuentres en el camino. Por ejemplo, con `MatSci18` la ejecución inicialmente se estancó en un puntaje muy negativo sin evolucionar; en la [conversación del laboratorio original](conversation.md) puedes ver cómo se diagnosticó y se corrigió.

### Opción B: Optimización de prompts

En [`example_prompt_optimization/`](./example_prompt_optimization/README.md) encontrarás un laboratorio completo e independiente de **optimización de prompts** cuantitativa, que comienza con ingeniería de prompts manual y avanza hasta la búsqueda evolutiva en lazo cerrado con OpenEvolve.

**Planteamiento del problema y del benchmark:**
- **Tarea**: evolucionar un programa de prompt parametrizado (`build_messages(ticket_text)`) que instruye a un LLM para clasificar tickets de soporte empresarial y extraer JSON estructurado (`intent_labels`, `urgency`, `sentiment`, `extracted_entities` y `requires_human_escalation`).
- **Conjunto de datos adversarial ([`dataset.py`](./example_prompt_optimization/dataset.py))**: 18 tickets seleccionados que cubren 6 modos de falla (`sarcasm_outage`, `multi_intent`, `resolved_negation`, `security_pii`, `entity_edge_cases` y `benign_routine`), además de una compuerta rápida (*canary gate*) de Etapa 1 con 5 tickets.
- **Evaluador ([`evaluator.py`](./example_prompt_optimization/evaluator.py))**: califica el F1 multietiqueta, la urgencia, el sentimiento, la extracción de entidades, el escalamiento a un humano y el formato JSON limpio, aplicando una penalización por exceso de tokens y retornando **artefactos** de diagnóstico.

**Ejercicios prácticos progresivos ([guía completa](./example_prompt_optimization/README.md)):**
1. **Inspecciona, evalúa y supera manualmente la línea base**: rastrea cómo se califica cada ticket, evalúa `initial_program.py` y diseña a mano un prompt mejorado en [`manual_prompt_attempt.py`](./example_prompt_optimization/manual_prompt_attempt.py).
2. **Autopsia de los modos de falla por categoría**: diagnostica por qué arreglar una categoría a mano (por ejemplo, sarcasmo o falsas alarmas ya resueltas) a menudo empeora el *recall* multi-intención o la extracción de montos en disputa frente a montos totales.
3. **El poder de la retroalimentación con artefactos (evolución ciega vs. gradientes textuales)**: realiza un experimento A/B que compare la evolución ciega con un único escalar (`--no-artifacts`) contra la evolución guiada por artefactos, en la que `category_accuracy_summary` y `failure_cases_report` le entregan al LLM mutador las diferencias exactas a nivel de campo.
4. **Calidad-diversidad y exploración de Pareto con MAP-Elites**: explora la frontera de Pareto entre precisión y presupuesto de tokens en grillas de características 2D (`prompt_char_length` $\times$ `few_shot_count`, o `--feature-dims` personalizadas).
5. **Personalización de la función de aptitud y de la compuerta en cascada**: ajusta las penalizaciones por presupuesto de tokens en `evaluator.py` y los umbrales de poda en cascada de la Etapa 1 en `config.yaml`.
