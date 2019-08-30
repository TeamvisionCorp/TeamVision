import psutil
import sys,os

process_name_list=['uwsgi']

def kill_process():
    for process_name in process_name_list:
        result=get_process(process_name)
        for process in result:
            print(process.name())
            process.kill()

def get_process(process_name):
    result=list()
    process_list =psutil.process_iter()
    for process in process_list:
        print(process.name())
        if process.name()==process_name:
            result.append(process)
    return result


if __name__ == '__main__':
    kill_process()


