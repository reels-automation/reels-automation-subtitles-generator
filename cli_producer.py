import json
from quixstreams import Application
from message.message import MessageBuilder


def main():

    app_producer = Application(broker_address="localhost:9092", loglevel="DEBUG")


    with app_producer.get_producer() as producer:
        tema = "holas"
        idioma="es"
        personaje = "Homero Simpson"
        usuario="43eda5b3-1c2b-424b-b460-c4d49198fc99"
        script = "Este es un mensaje de prueba"
        audio_item=[{"tts_audio_name": "tema_at_1751469037_327388_2025-07-02_15_10_47_298969.mp3", 
                    "tts_audio_directory": "audios-tts",
                    "file_getter": "minio", 
                    "pitch": 0, 
                    "tts_voice": "es-ES-XimenaNeural",
                    "tts_rate": 0, 
                    "pth_voice": "homero"}]
        gameplay_name="subway.mp4"
        message_builder = MessageBuilder(tema)
        message = (message_builder
                   .add_personaje(personaje)
                   .add_script(script)
                   .add_usuario(usuario)
                   .add_idioma(idioma)
                   .add_audio_item(audio_item)
                   .add_gameplay_name(gameplay_name)
                   .add_random_images("False")
                   .build())
        
        while True:
            input("Enviar mensaje de prueba: \n")
            producer.produce(
                topic="audio_subtitles", key="temas_input_humano", value=json.dumps(message.to_dict()))            

if __name__ == "__main__":
    main()
