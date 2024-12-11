import ast
from quixstreams import Application
from subtitle_saver.i_subtitle_saver_strategy import ISubtitleSaverStrategy
from subtitles_generator.i_subtitle_generator import ISubtitleGenerator

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
           #     print("Message Value: ", msg.value())
                consumer.store_offsets(msg)
                msg_value_json_response = ast.literal_eval(msg.value().decode("utf-8"))
            #    print(msg_value_json_response)
                audio_name = msg_value_json_response["audio_name"]
                bucket_name = ["bucket_name"]

                file_path = subtitle_saver.get_file(audio_name)

                subtitle_generator.create_subtitles(file_path,subtitle_saver)
                #subtitle_saver.save_subtitle(audio_name, bucket_name)
                #print(msg_value_json_response)

            


