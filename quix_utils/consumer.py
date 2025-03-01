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
                audio_name = msg_value_json_response["tts_audio_name"]

                file_path = subtitle_saver.get_file(audio_name)
                subtitles_file_name = subtitle_generator.create_subtitles(file_path,subtitle_saver)
                subtitles_bucket = subtitle_saver.subtitles_bucket_name

                message_builder = MessageBuilder(msg_value_json_response["tema"])
                message = (message_builder
                            .add_personaje(msg_value_json_response["personaje"])
                            .add_script(msg_value_json_response["script"])
                            .add_tts_audio_name(audio_name)
                            .add_tts_audio_bucket(msg_value_json_response["tts_audio_bucket"])
                            .add_subtitles_name(subtitles_file_name)
                            .add_subtitles_bucket(subtitles_bucket)
                            .add_author(msg_value_json_response["author"])
                            .add_pitch(msg_value_json_response["pitch"])
                            .add_tts_voice(msg_value_json_response["tts_voice"])
                            .add_tts_rate(msg_value_json_response["tts_rate"])
                            .add_pth_voice(msg_value_json_response["pth_voice"])
                            .add_gameplay_name(msg_value_json_response["gameplay_name"])
                            .build()
                        )
                
                
                app_producer = Application(
                    broker_address=KAFKA_BROKER, loglevel="DEBUG"
                )
                topic_to_produce = "subtitles-audios"
                key = "consumer-subtitles"
                data = str(message.to_dict())
                create_producer(app_producer,topic_to_produce,key,data)

