import json
from logs import logging



class Data:

    def opener(path, file_name, operation, **kwargs):
        file_path = f"{path}/{file_name}"

        try:
            if operation == "a":
                with open(file_path, operation, encoding="utf-8") as f:
                    data_to_write = kwargs.get("json_file")
                    json_str = json.dumps(data_to_write, ensure_ascii=False)
                    f.write(json_str + "\n")
                    return True

            elif operation == "r":
                with open(file_path, operation, encoding="utf-8") as f:
                    lines = f.readlines()
                    return lines
                
            else:
                logging.error(f"Invalid operation: {operation}")
                return None

        except FileNotFoundError:
            logging.exception(f"Message from {__file__}: File {file_name} not found.")
            return None
        
        except json.JSONDecodeError as e:
            logging.exception(f"JSON decoding error: {e}")
            return None
        
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            return None
    