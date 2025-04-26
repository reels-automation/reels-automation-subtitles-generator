import ast
from quixstreams import Application
from subtitle_saver.i_subtitle_saver_strategy import ISubtitleSaverStrategy
from subtitles_generator.i_subtitle_generator import ISubtitleGenerator
from quix_utils.producer import create_producer
from message.message import MessageBuilder
from setttings import KAFKA_BROKER

def create_consumer(app_consumer: Application, topic_to_subscribe: str, subtitle_saver:ISubtitleSaverStrategy, subtitle_generator: ISubtitleGenerator):
    with app_consumer.get_consumer() as consumer:
        consumer.subscribe([topic_to_subscribe])
        while True:
            msg = consumer.poll(1)
            if msg is None:
                print("Waiting...")
            elif msg.error() is not None:
                raise ValueError(msg.error())
            else:
                consumer.store_offsets(msg)
                msg_value_json_response = ast.literal_eval(msg.value().decode("utf-8"))
                
                print("Msg value json response: ", msg_value_json_response)
                audio_name = msg_value_json_response["audio_item"][0]["tts_audio_name"]

                file_path = subtitle_saver.get_file(audio_name)
                print("File path: ", file_path)
                if file_path is not None:

                    subtitles_file_name = subtitle_generator.create_subtitles(file_path,subtitle_saver)
                    subtitles_bucket = subtitle_saver.subtitles_bucket_name

                    subtitles_item_save = [{
                    "subtitles_name": subtitles_file_name,
                    "file_getter": "minio",
                    "subtitles_directory": subtitles_bucket
                    }]

                    message_builder = MessageBuilder(msg_value_json_response["tema"])
                    message = (message_builder
                                    .add_usuario(msg_value_json_response["usuario"])
                                    .add_idioma(msg_value_json_response["idioma"])
                                    .add_personaje(msg_value_json_response["personaje"])
                                    .add_script(msg_value_json_response["script"])
                                    .add_audio_item(msg_value_json_response["audio_item"])
                                    .add_subtitle_item(subtitles_item_save)
                                    .add_author(msg_value_json_response["author"])
                                    .add_gameplay_name(msg_value_json_response["gameplay_name"])
                                    .add_background_music(msg_value_json_response["background_music"])
                                    .add_images(msg_value_json_response["images"])
                                    .add_random_images(msg_value_json_response["random_images"])
                                    .add_random_amount_images(msg_value_json_response["random_amount_images"])
                                    .add_gpt_model(msg_value_json_response["gpt_model"])
                                    .build()
                            )
                
                    app_producer = Application(
                        broker_address=KAFKA_BROKER, loglevel="DEBUG"
                    )
                    topic_to_produce = "subtitles-audios"
                    key = "consumer-subtitles"
                    data = str(message.to_dict())
                    create_producer(app_producer,topic_to_produce,key,data)

