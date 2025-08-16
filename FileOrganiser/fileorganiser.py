import shutil
import os




FILE_CATEGORIES = {
    "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
    "Documents": ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf', '.odt'],
    "Audio": ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'],
    "Videos": ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm'],
    "Archives": ['.zip', '.rar', '.7z', '.tar', '.gz'],
    "Executables & Installers": ['.exe', '.msi', '.dmg', '.pkg'],
    "Other": [] # This is a fallback for any file type not listed above.
}
target_paths=["C:\\Users\\USER\\Downloads","C:\\Users\\USER\\Documents"]

def organize_files(path):
        print('Started the organization')
        

        try:
            list_of_entries=os.listdir(path)
        except Exception as e:
            print('File was not found,{e}')
            return


        for entry in list_of_entries:
            entry_path=os.path.join(path,entry)
            if os.path.isdir(entry_path):
                organize_files(entry_path)

            elif os.path.isfile(entry_path):
                try:
                    file_extension=os.path.splitext(entry)[1].lower()
                except Exception as e:
                    file_extension=" "
                destination_folder_name='Other'
            
                for foldername,extensions in FILE_CATEGORIES.items():
                    if file_extension in extensions:
                        destination_folder_name=foldername
                        break
                destination_folder_path=os.path.join(path,destination_folder_name)

                if not os.path.exists(destination_folder_path):
                    os.makedirs(destination_folder_path)
                try:
                    shutil.move(entry_path,destination_folder_path)
                except Exception as e:
                    print(f'Could not move {entry_path} to {destination_folder_path}')
        
if __name__=="__main__":
    for target_path in target_paths:
        organize_files(target_path)
        print("finished organizing the files")