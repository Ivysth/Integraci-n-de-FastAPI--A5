import reflex as rx
import requests


class State(rx.State):

    pregunta: str = ""

    historial: list[dict] = []

    def set_pregunta(self, value: str):
        self.pregunta = value

    def enviar(self):

        if not self.pregunta.strip():
            return

        pregunta_usuario = self.pregunta

        # Agregar mensaje del usuario
        self.historial.append(
            {
                "tipo": "usuario",
                "texto": pregunta_usuario,
            }
        )

        # Limpiar input
        self.pregunta = ""

        try:

            r = requests.post(
                "http://127.0.0.1:8001/preguntar",
                json={"mensaje": pregunta_usuario},
                timeout=60,
            )

            if r.status_code == 200:

                respuesta = r.json().get(
                    "respuesta",
                    "Sin respuesta"
                )

            else:

                respuesta = f"Error API ({r.status_code}): {r.text}"

        except Exception as e:

            respuesta = f"Error conexión: {str(e)}"

        # Agregar respuesta IA
        self.historial.append(
            {
                "tipo": "ia",
                "texto": respuesta,
            }
        )


def mensaje(msg):

    es_usuario = msg["tipo"] == "usuario"

    return rx.flex(

        rx.cond(
            es_usuario,
            rx.spacer(),
            rx.fragment(),
        ),

        rx.box(
            rx.text(
                msg["texto"],
                white_space="pre-wrap",
            ),
            bg=rx.cond(
                es_usuario,
                "#2563eb",
                "#f3f4f6",
            ),
            color=rx.cond(
                es_usuario,
                "white",
                "black",
            ),
            padding="12px",
            border_radius="12px",
            max_width="75%",
        ),

        rx.cond(
            es_usuario,
            rx.fragment(),
            rx.spacer(),
        ),

        width="100%",
        margin_bottom="10px",
    )


def index():

    return rx.center(

        rx.vstack(

            rx.heading(
                "Chat con Gemini",
                size="7",
                color="#1f2937",
                text_align="center",
                width="100%",
            ),

            # Historial de conversación
            rx.box(

                rx.foreach(
                    State.historial,
                    mensaje,
                ),

                width="100%",
                height="75vh",
                overflow_y="auto",
                border="1px solid #d1d5db",
                border_radius="12px",
                padding="15px",
                bg="white",
            ),

            # Barra inferior
            rx.hstack(

                rx.input(
                    placeholder="Escribe tu pregunta...",
                    value=State.pregunta,
                    on_change=State.set_pregunta,
                    width="100%",
                ),

                rx.button(
                    "Enviar",
                    on_click=State.enviar,
                ),

                width="100%",
            ),

            width="80%",
            max_width="1000px",
            spacing="4",
            padding="20px",
        ),

        width="100%",
        height="100vh",
        bg="#f8fafc",
    )


app = rx.App()
app.add_page(index)