from .processor import Processor, YoutubeProcessor, FileProcessor
def initialize_routes(api):
    api.add_resource(Processor, '/api/processor')
    api.add_resource(YoutubeProcessor, '/api/processor/youtube')
    api.add_resource(FileProcessor, '/api/processor/file')