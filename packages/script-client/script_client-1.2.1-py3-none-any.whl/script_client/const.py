


class Config:
    def __init__(self):
        self.local_ip='127.0.0.1'
        self.local_port = 7788
        self.client_name = 'xyz'
        self.regist_server_url = r'https://www.baidu.com/'
        self.heart_beat_url = r'https://www.baidu.com/'
        self.result_url = r'https://www.baidu.com/'
        self.http_request_timeout = 1
        self.max_thread = 100
        self.max_task = 2000
        self.test_script_dir = r'D:\1\ts'
        self.py_timeout = 15
        self.robot_url = ''
        self.work_path=''
        pass


config = Config()






class FMap:
    def __init__(self):
        self.func_map = {}
        # '''
        # func_map = {
        #     'omc':{
        #         '/omc/mark/path1':[
        #             {'函数对象':'timeout'},
        #             {'函数对象':'timeout'}
        #         ],
        #         '/omc/mark/path2':[
        #             {'函数对象':'timeout'},
        #             {'函数对象':'timeout'}
        #         ]
        #     },
        #     'ofc':{
        #         '/ofc/path1':[
        #             {'函数对象':'timeout'},
        #             {'函数对象':'timeout'}
        #         ],
        #         '/ofc/path2':[
        #             {'函数对象':'timeout'},
        #             {'函数对象':'timeout'}
        #         ]
        #     }
        # }
        # '''

    def add_map(self,app,path,func,timeout):
        if app not in self.func_map:
            self.func_map[app] = {path:[{func:timeout}]}
        else:
            t_dict = self.func_map[app]
            if path not in t_dict:
                self.func_map[app][path] = [{func: timeout}]
            else:
                self.func_map[app][path].append({func: timeout})


    def get_map(self):
        return self.func_map


fm = FMap()