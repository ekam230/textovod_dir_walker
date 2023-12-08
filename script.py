import os,time,signal,pathlib
from req import send_request

pause_time = 5

result = list(pathlib.Path(".").rglob("*.[tT][xX][tT]"))
print(f'Total files find: {len(result)} files')

dir = "Results" #name of dir result
  
# Parent Directory path 
parent_dir =  os.path.abspath(os.curdir)
  
# Path 
path = os.path.join(parent_dir, dir) 

# Рекурсивная функция для удаления папки

def del_folder(path):

    for sub in path.iterdir():
        if sub.is_dir():
            # Удалить каталог, если он является подкаталогом
            del_folder(sub)
        else :
            # Удалить файл, если это файл:
            sub.unlink()
    
    # Удалить папку верхнего уровня:
    path.rmdir()


if pathlib.Path(path).exists():
    print("Directory already exists. Need delete. Delete? y/n")
    if input() == 'y':
        del_folder(pathlib.Path(path))
        print('Directory succefuly removed.')
    else:
        print('Exit')
        exit(1)        
else:
    print("Directory does not exist")
  
# Create the directory 
try:  
    os.mkdir(path)  
except OSError as error:  
    print(error)   

id = 0
list_files = []

for i in result:    
    filepath_from = os.path.join(i.parts[0],i.name)
          
    subdir = os.path.join(dir,i.parts[0])
    filepath = os.path.join(subdir,i.name)
    
    
    # checking if the directory 
    # exist or not. 
    if not os.path.exists(subdir):         
        # if the folder directory is not present  
        # then create it. 
        os.makedirs(subdir)        
    
    with open(filepath_from, 'r', encoding='utf-8') as r:
        data = r.read()
    
    data_file = [id, i.parts[0], i.name, data]     
    list_files.append(data_file)    
    id = id+1

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':        
        exit(1)
 
signal.signal(signal.SIGINT, handler)

list_files_status_0 = []
list_files_status_1 = []
list_files_status_2 = []
list_files_status_3 = []

while len(list_files) !=0:
    for i in list_files:
        req = send_request(i[3]) #send request
        if req['status'] == 3: # status 3 =  queue
            list_files_status_3.append(i)
        if req['status'] == 2: #status 2 == welldone
            list_files_status_2.append(i)
            list_files_status_2[-1].append(req["status"])
            list_files_status_2[-1].append(req["originality"])
            list_files_status_2[-1].append(req["text_id"])
            list_files.remove(i)
        if req['status'] == 0: #status 0 error
            list_files_status_0.append(i)
        if req['status'] == 1: #status 1 wait
            list_files_status_1.append(i)
        
        print('Errors ', len(list_files_status_0),'files')
        print('Wait ', len(list_files_status_1),'files')
        print('Queue ', len(list_files_status_3),'files')
        print('Welldone ', len(list_files_status_2),'files')
        
        time.sleep(1)
        
        
        # print(f'There are still files left {len(list_files)}')
    
    
    if len(list_files) == 0:
        break
    print('Little pause ', pause_time, 'sec')
    time.sleep(pause_time)
    print("pause left")
    

while len(list_files_status_2) !=0:
    for i in list_files_status_2:
        if i[4] == 2:
            dir_path = os.path.join(dir,i[1])            
            add_originality_to_path = str(i[5])
            filepath = os.path.join(dir_path,add_originality_to_path + '_' + i[2])
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(i[3])
            list_files_status_2.remove(i)
            
print("Well done")