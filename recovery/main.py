import json
import re
import os, string
import codecs

class FileRecovery():
    def __init__(self, file_extension: str, drive: str, destiny: str):
        self.file_extension= file_extension
        self.drive = drive
        self.destiny = destiny
    
    def __load_signatures_database(self):
        with open(r'E:\1. INGENIERIA DE SISTEMAS\3. PORTFOLIO\RECOVERY\recovery\signatures.json', 'r') as json_signatures_file:
            return json.load(json_signatures_file)[self.file_extension]
        pass

    def __get_trail_signature(self, signatures_repo) -> str:
        return signatures_repo['end']

    def __get_beginning_signature(self, signatures_repo) -> str:
        return signatures_repo['beginning']
    
    def __get_extras_signatures(self, signatures_repo) -> list:
        return signatures_repo['extras']
    
    def __format_signatures(self, list_unformatted: list[dict] | None) -> list:
        if list_unformatted:
            formatted = []
            for sig in list_unformatted:
                beginning = codecs.decode(sig['beginning'], 'unicode_escape').encode('latin1')
                end = codecs.decode(sig['end'], 'unicode_escape').encode('latin1')
                formatted.append({"beginning": beginning, "end": end})
            return formatted
        return []

    def __get_available_drives(self):
        return ['%s:'%d for d in string.ascii_uppercase if os.path.exists('%s:'%d)]

    def __check_drive(self) -> bool:
        return self.drive in self.__get_available_drives()
    
    def __recovery(self, start: str, end: str, extras_end: list) -> None:
        print(extras_end)
        counter_coincidencia = 0
        file_content = True
        beginning_trail_bytes = bytes.fromhex(start.replace('\\x', ''))
        ending_trail_bytes = bytes.fromhex(end.replace('\\x', ''))
        with open(f'\\\\.\\{self.drive}', 'rb') as drive_recover:
            while file_content:
                file_content = drive_recover.read(512)
                tail = file_content[-(len(ending_trail_bytes) + 5):]
                file_content = tail + drive_recover.read(512)
                find = file_content.find(beginning_trail_bytes)
                if find != -1:
                    print(file_content)
                    print('find')
                    saving = True
                    with open(f'{self.destiny}/{counter_coincidencia}.{self.file_extension}', 'wb') as destiny_file:
                        destiny_file.write(file_content[find:])
                        while saving:
                            file_content = drive_recover.read(512)
                            find = file_content.find(ending_trail_bytes)
                            if find == -1:
                                destiny_file.write(file_content)
                            else:
                                saved_extra = False
                                if extras_end:
                                    extra_found = []
                                    for extra in extras_end:
                                        new_signature = extra['beginning'] + ending_trail_bytes + extra['end']
                                        print(new_signature)
                                        find_extra = file_content.find(new_signature)
                                        if find_extra != -1:
                                            extra_found.append(new_signature)
                                    if extra_found:
                                        signature = max(extra_found, key=len)
                                        start_pos = file_content.find(signature)
                                        destiny_file.write(file_content[:start_pos])
                                        saved_extra = True
                                        print(extra_found)
                                if not saved_extra:
                                    destiny_file.write(file_content[:find])
                                saving = False
                                print(f"guardado archivo: {counter_coincidencia}")
                                counter_coincidencia += 1

                    

                                

                

    def start_recovery(self):
        signatures_db = self.__load_signatures_database()
        start, end = self.__get_beginning_signature(signatures_db), self.__get_trail_signature(signatures_db)
        extras_clean = self.__format_signatures(self.__get_extras_signatures(signatures_db))
        if self.__check_drive():
            self.__recovery(start, end, extras_clean)
    

# Only for testing
if __name__ == '__main__':
    FileRecovery('pdf', 'D:', 'E:/').start_recovery()