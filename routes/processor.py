from controllers.processor import file_processor
from controllers.processor import youtube_processor
from flask_restful import Resource,reqparse
import datetime

class Processor(Resource):
    def get(self):
        return {
            'message': 'pong',
            'timestamp': '{}'.format(datetime.datetime.now())
        }

class YoutubeProcessor(Processor):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('video_id',type=str)
        args=parser.parse_args()
        return youtube_processor(args)

class FileProcessor(Processor):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file_path',type=str)
        args=parser.parse_args()
        return file_processor(args)
