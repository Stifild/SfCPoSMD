import json, logging

logging.basicConfig(
    filename="./logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)

class Utils:

    @staticmethod
    def load_json(file_path):
        try:
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                return data
        except Exception as e:
            logging.error("Не удалось выполнить запрос (Utils.read_json):", e)
            return {}

    @staticmethod
    def save_json(file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f)

    def load_config(self, file_path='config.json'):
        return self.load_json(file_path)
