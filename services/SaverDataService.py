import os


class SaverDataService:
    saved_data_path = os.getcwd() + '/svd.d'

    @staticmethod
    def save_state():
        return None

    @staticmethod
    def load_state():
        return None
