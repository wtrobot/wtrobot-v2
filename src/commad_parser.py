import os,sys
import logging 
from yaml import load, dump
import src

class commmandParser:
    
    def __init__(self, global_conf):

        self.global_conf = global_conf
        self.testscript = self.yaml_loader(filepath=self.global_conf["script_filepath"])
        self.obj_action = src.Actions(self.global_conf)
        if not os.path.exists("./tmp"):
            os.makedirs("./tmp")

        # initate parser
        self.testscript_parser()

    def yaml_loader(self, filepath):
        ''' Read yaml file and return the dict '''
        
        logging.info('Reading script yml file')
        # self.logger.info("loaded file...")
        data = dict()
        if os.path.isfile(filepath):
            with open(filepath, "r") as obj:
                data = load(obj)
            if not data:
                return dict()
        else:
            logging.error("invalid file {}".format(filepath))
            sys.exit(0)            
        return data

    def yaml_dump(self, filepath, data):
        ''' Write the dict to yaml file '''
        with open(filepath, "w") as obj:
            dump(data, obj, default_flow_style=False)

    def testcase_parser(self, testcase_dict, testcase_no=0):
        '''
        This function will iterate through single testcase and execute it 
        '''
        for step in testcase_dict.keys():
                # block of single testcase
                if isinstance(testcase_dict[step], dict):
                    # import testcase within testcase
                    if testcase_dict[step]["action"] == "import":
                        if "target" in testcase_dict[step].keys() and testcase_dict[step]["target"] in self.testscript.keys():
                            # recursive call
                            self.testcase_parser(self.testscript[testcase_dict[step]["target"]],testcase_no=testcase_dict[step]["target"])
                        else:
                            logging.error("Testcase number or import target value incorrect/missing in {} at {}".format(testcase_no,step))
                    
                    # check if mentioned action is supported by WTRobotv2
                    elif testcase_dict[step]["action"] in dir(self.obj_action):
                        # adding testcase no and step_no just to keep track of execution
                        testcase_dict[step]["step_no"] = step
                        testcase_dict[step]["testcase_no"] = testcase_no 
                        # call respective function
                        testcase_dict[step] = getattr(self.obj_action, testcase_dict[step]["action"])(testcase_dict[step])
                        # cleanup
                        testcase_dict[step].pop("step_no")                       
                        testcase_dict[step].pop("testcase_no")

                        if "error" in testcase_dict[step].keys() and testcase_dict[step]["error"] == True:
                            testcase_dict[step].pop("error")
                            logging.warning("Exiting testcase:{} due to failure in step:{}".format(testcase_no,step))
                            break

                    else:
                        logging.error("INVALID COMMAND '{}' in {} at {}".format(testcase_dict[step]["action"], testcase_no, step))

                # senario tag of single testcase
                elif isinstance(testcase_dict["scenario"], str):
                    logging.info("Executing scenario: {}".format(testcase_dict["scenario"]))
                
                else:
                    logging.error("INVALID COMMAND '{}' in {} at {}".format(testcase_dict[step]["action"], testcase_no, step))

        return testcase_dict

    def testscript_parser(self):
        '''
        This function will iterate through entire testscript dict from test file 
        '''
        logging.info("command parser init")
        testcase_list = list()
        # if sequence key is mentioned then follow the sequence else the dict sequence  
        if "sequence" in self.testscript.keys(): 
            testcase_list = self.testscript["sequence"]
        else: 
            testcase_list = self.testscript.keys()

        for testcase in testcase_list:
            self.testscript[testcase] = self.testcase_parser(testcase_dict=self.testscript[testcase],testcase_no=testcase)
        
        # update script file 
        self.yaml_dump(filepath=self.global_conf["script_filepath"], data=self.testscript)
