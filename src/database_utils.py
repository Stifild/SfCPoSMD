import logging, sqlite3
from src.utils import Utils

io = Utils()
config = io.load_config()

DB_PATH = config["DB_PATH"]
TABLE_NAME = config["TABLE_NAME"]

class Database:
    def __init__(self):
        self.create_table()

    def executer(self, command: str, data: tuple = None):
        try:
            self.connection = sqlite3.connect(DB_PATH)
            self.cursor = self.connection.cursor()

            if data:
                self.cursor.execute(command, data)

            else:
                self.cursor.execute(command)

        except Exception as e:
            logging.error(f"Ошибка при выполнении запроса (DataBase.executer): {e}")

        self.connection.commit()
        result = self.cursor.fetchall()
        self.connection.close()
        return result

    def create_table(self):
        try:
            self.executer(
                f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME}
                (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                grade TEXT,
                phone TEXT,
                first_lesson TEXT,
                second_lesson TEXT
                third_lesson TEXT,
                fourth_lesson TEXT,
                fifth_lesson TEXT,
                sixth_lesson TEXT,
                seventh_lesson TEXT
                );
                """
            )
            logging.info(f"Таблица {TABLE_NAME} создана")
        except Exception as e:
            logging.error("Ошибка при создании таблицы: ", e)
            exit(1)
    def add_user(self, user_id: int, username: str):
        """
        Adds a new user to the database.

        Args:
            user_id (int): The ID of the user.
            username (str): The username of the user.
        """
        try:
            self.executer(
                f"INSERT INTO {TABLE_NAME} (user_id, username) VALUES ({user_id}, {username});"
                )
            logging.debug(f"Добавлен пользователь {user_id}")
        except Exception as e:
            logging.error(
                f"Возникла ошибка при добавлении пользователя {user_id} (DataBase.add_user): {e}"
            )

    def check_user(self, user_id: int) -> bool:
        """
        Checks if a user exists in the database.

        Args:
            user_id (int): The ID of the user.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        try:
            result = self.executer(
                f"SELECT user_id FROM {TABLE_NAME} WHERE user_id=?;", (user_id,)
            )
            return bool(result)
        except Exception as e:
            logging.error(f"Возникла ошибка при проверке пользователя {user_id}: {e}")

    def update_value(self, user_id: int, column: str, value):
        """
        Updates a value for a specific user in the database.

        Args:
            user_id (int): The ID of the user.
            column (str): The name of the column to update.
            value: The new value for the column.
        """
        try:
            self.executer(
                f"UPDATE {TABLE_NAME} SET {column}=? WHERE user_id=?;", (value, user_id)
            )
            logging.info(f"Обновлено значение {column} для пользователя {user_id}")
        except Exception as e:
            logging.error(
                f"Возникла ошибка при обновлении значения {column} для пользователя {user_id}: {e}"
            )

    def get_user_data(self, user_id: int) -> dict:
            try:
                result = self.executer(
                    f"SELECT * FROM {TABLE_NAME} WHERE user_id=?;", (user_id,)
                )
                if result:
                    presult = {
                        "first_name": int(result[0][2]),
                        "last_name": int(result[0][3]),
                        "username": int(result[0][4]),
                        "grade": int(result[0][5]),
                        "phone": int(result[0][6]),
                        "first_lesson": int(result[0][7]),
                        "second_lesson": int(result[0][8]),
                        "third_lesson": int(result[0][9]),
                        "fourth_lesson": int(result[0][10]),
                        "fifth_lesson": int(result[0][11]),
                        "sixth_lesson": int(result[0][12]),
                        "seventh_lesson": int(result[0][13]),
                    }
                    return presult
                else:
                    logging.error(f"Пользователь {user_id} не найден в базе данных вернулся пустой словарь")
                    return {}
            except Exception as e:
                logging.error(
                    f"Возникла ошибка при получении данных пользователя {user_id}: {e}"
                )
                return {}

    def get_all_users(
        self,
    ) -> list[tuple]:
        """
        Retrieves the data for all users from the database.

        Returns:
            list[tuple]: A list of tuples containing the user data.
        """
        try:
            result = self.executer(f"SELECT * FROM {TABLE_NAME};")
            return result
        except Exception as e:
            logging.error(
                f"Возникла ошибка при получении данных всех пользователей: {e}"
            )

    def delete_user(self, user_id: int):
        """
        Deletes a user from the database.

        Args:
            user_id (int): The ID of the user.
        """
        try:
            self.executer(f"DELETE FROM {TABLE_NAME} WHERE user_id=?;", (user_id,))
            logging.warning(f"Удален пользователь {user_id}")
        except Exception as e:
            logging.error(f"Возникла ошибка при удалении пользователя {user_id}: {e}")

if __name__ == "__main__":
    Database().create_table()