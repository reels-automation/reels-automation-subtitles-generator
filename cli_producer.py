from quixstreams import Application
from message.message import MessageBuilder


def main():

    app_producer = Application(broker_address="localhost:9092", loglevel="DEBUG")


    with app_producer.get_producer() as producer:
        tema = "Mensaje de prueba subtilos"
        personaje = "Homero Simpson"
        script = "Este es un mensaje de prueba"
        audio_bucket = "audios-tts"
        tts_audio_name = "Mensaje_de_prueba_2025-03-01_14_42_06_872752.mp3"

        message_builder = MessageBuilder(tema)
        message = (message_builder
                   .add_personaje(personaje)
                   .add_script(script)
                   .add_tts_audio_bucket(audio_bucket)
                   .add_tts_audio_name(tts_audio_name)
                   .build())
        
        while True:
            input("Enviar mensaje de prueba: \n")
            producer.produce(
                topic="audio_subtitles", key="temas_input_humano", value=str(message.to_dict())
            )


if __name__ == "__main__":
    main()
