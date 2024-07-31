from logs import logging



class Data:

    def opener(path, file_name, operation, **kwargs):
        try:
            json_str = kwargs.get("json_file")
            
            if operation == "a":
                with open(f"{path}/{file_name}", operation, encoding="utf-8") as f:
                    f.write(json_str + "\n")
                    return f
                
            elif operation == "r":
                with open(f"{path}/{file_name}", operation, encoding="utf-8") as f:
                    lines = f.readlines()
                    return lines

        except FileNotFoundError:
            return logging.exception(f"Message from {__file__}: File {file_name} not found.")
        