import json
import re
import os, string


class FileRecovery():
    def __init__(self, file_extension: str, drive: str, destiny: str):
        self.file_extension= file_extension
        self.drive = drive
        self.destiny = destiny
    
    def __load_signatures_database(self):
        with open(r'signatures.json', 'r') as json_signatures_file:
            return json.load(json_signatures_file)[self.file_extension]
        pass

    def __get_trail_signature(self, signatures_repo) -> str:
        return signatures_repo['end']

    def __get_beginning_signature(self, signatures_repo) -> str:
        return signatures_repo['beginning']
    
    def __get_available_drives(self):
        return ['%s:'%d for d in string.ascii_uppercase if os.path.exists('%s:'%d)]

    def __check_drive(self) -> bool:
        return self.drive in self.__get_available_drives()
    
    def __recovery(self, start: str, end:str):
        counter_coincidencia = 0
        file_content = True
        beginning_trail_bytes = bytes.fromhex(start.replace('\\x', ''))
        ending_trail_bytes = bytes.fromhex(end.replace('\\x', ''))
        tail = b''
        with open(f'\\\\.\\{self.drive}', 'rb') as drive_recover:
            while file_content:
                file_content = drive_recover.read(512)
                tail = file_content[-len(beginning_trail_bytes):]
                find = re.search(beginning_trail_bytes, file_content)
                if find:
                    saving = True
                    with open(f'{self.destiny}/{counter_coincidencia}.{self.file_extension}', 'wb') as destiny_file:
                        destiny_file.write(file_content[find.start():])
                        while saving:
                            file_content = drive_recover.read(512)
                            find = re.search(ending_trail_bytes, file_content)
                            if not find: 
                                destiny_file.write(file_content)
                            else:
                                # Acá código de firma
                                saving = False
                                counter_coincidencia += 1
                    

                                

                

    def start_recovery(self):
        signatures_db = self.__load_signatures_database()
        start, end = self.__get_beginning_signature(signatures_db), self.__get_trail_signature(signatures_db)
        if self.__check_drive():
            self.__recovery(start, end)
        else:
            pass

    

# Only for testing
if __name__ == '__main__':
    FileRecovery('jpg', 'D:', 'E:/').start_recovery()