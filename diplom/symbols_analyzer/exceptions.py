class BadResolution(Exception):

    def __init__(self):
        self.message = (
            'Ошибка чтения изображения. Возможные причины проблемы:\n'
            '1. Изображение сфотографировано не ровно.\n'
            '2. Изображение сфотографировано при плохом освещение'
        )