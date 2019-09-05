import os, sys
import logging
from collections import OrderedDict
from ruamel.yaml import YAML
import src


class commmandParser:
    def __init__(self, global_conf):

        self.yaml = YAML()
        self.yaml.indent(1)
        self.yaml.explicit_start = True

        self.global_conf = global_conf
        self.testscript = self.yaml_loader(filepath=self.global_conf["script_filepath"])
        self.obj_action = src.Actions(self.global_conf)
        if not os.path.exists("./tmp"):
            os.makedirs("./tmp")

        # initate parser
        self.testscript_parser()

    def yaml_loader(self, filepath):
        """ Read yaml file and return the dict """

        logging.info("Reading script yml file")
        data = dict()
        if os.path.isfile(filepath):
            with open(filepath, "r") as obj:
                data = self.yaml.load(obj)
            if not data:
                return dict()
        else:
            logging.error("invalid file {0}".format(filepath))
            sys.exit(0)
        return data

    def yaml_dump(self, filepath, data):
        """ Write the dict to yaml file """
        with open(filepath, "w") as obj:
            self.yaml.dump(data, obj)

    def testcase_parser(self, testcase_list, testcase_no):
        """
        This function will execute all steps from single testcase
        """

        step_list = list()
        for step in testcase_list:
            step_list.append(list(step.keys())[0])

        # if scenario tag not specifed then add empty tag to avoid exception
        if "scenario" not in step_list:
            step_list.insert(0, "scenario")
            tmpdict = OrderedDict([("scenario", None)])
            testcase_list.insert(0, tmpdict)

        for step in step_list:
            index = step_list.index(step)
            if step == "scenario":
                logging.info(
                    "Executing testcase: {0} - {1}".format(
                        testcase_no, testcase_list[0]["scenario"]
                    )
                )

            elif isinstance(testcase_list[index], dict):

                # if indentation for step elements are improper
                if not testcase_list[index][step]:
                    logging.error(
                        "Empty step or improper indentation for steps in yaml testscript"
                    )

                # if "targets" mentioned is str then convert to list
                if "targets" in testcase_list[index][step].keys() and isinstance(
                    testcase_list[index][step]["targets"], str
                ):
                    logging.error(
                        "Targets specified must be list in testcase:{0} step: {1} in yaml testscript".format(
                            testcase_no, step
                        )
                    )
                    tmp = testcase_list[index][step]["targets"]
                    testcase_list[index][step]["targets"] = list([tmp])

                # if "targets" not specified in yaml script then create a list and copy target value init
                if (
                    "targets" not in testcase_list[index][step].keys()
                    and "target" in testcase_list[index][step].keys()
                ):
                    testcase_list[index][step]["targets"] = list(
                        [testcase_list[index][step]["target"]]
                    )

                # if "targets" specified and no "target" then copy first element from targets
                elif (
                    "targets" in testcase_list[index][step].keys()
                    and "target" not in testcase_list[index][step].keys()
                ):
                    testcase_list[index][step]["target"] = testcase_list[index][step][
                        "targets"
                    ][0]

                # if action is import
                if testcase_list[index][step]["action"] == "import":
                    tmp_testcase_no = testcase_list[index][step]["target"]
                    index2 = self.global_testcase_no_list.index(tmp_testcase_no)
                    self.testscript["test"][index2][
                        tmp_testcase_no
                    ] = self.testcase_parser(
                        testcase_list=self.testscript["test"][index2][tmp_testcase_no],
                        testcase_no=tmp_testcase_no,
                    )

                # check if specified action exist
                elif testcase_list[index][step]["action"] in dir(self.obj_action):
                    testcase_list[index][step]["step_no"] = step
                    testcase_list[index][step]["testcase_no"] = testcase_no

                    # call respective function
                    method_name = testcase_list[index][step]["action"]
                    testcase_list[index][step] = getattr(self.obj_action, method_name)(
                        testcase_list[index][step]
                    )

                    # cleanup
                    testcase_list[index][step].pop("step_no")
                    testcase_list[index][step].pop("testcase_no")
                    if "element_obj" in testcase_list[index][step].keys():
                        testcase_list[index][step].pop("element_obj")

                    # Exit loop if error bit set for testcase
                    if (
                        "error" in testcase_list[index][step].keys()
                        and testcase_list[index][step]["error"] == True
                    ):
                        testcase_list[index][step].pop("error")
                        logging.warning(
                            "Exiting testcase:{0} due to failure in step:{1}".format(
                                testcase_no, step
                            )
                        )
                        break

                else:
                    logging.error(
                        "INVALID COMMAND '{0}' in {1} at {2}".format(
                            testcase_list[step_list.index(step)][step]["action"],
                            testcase_no,
                            step,
                        )
                    )

        return testcase_list

    def testscript_parser(self):
        """
        This function will iterate through entire testscript dict from test file 
        """
        logging.info("command parser init")

        sequence_testcase_no_list = list()
        self.global_testcase_no_list = list()

        for testcase in self.testscript["test"]:
            self.global_testcase_no_list.append(list(testcase.keys())[0])

        # if sequence key is mentioned then follow the sequence else the dict sequence
        if "sequence" in self.testscript.keys():
            sequence_testcase_no_list = self.testscript["sequence"]
        else:
            sequence_testcase_no_list = self.global_testcase_no_list

        for testcase in sequence_testcase_no_list:
            index = self.global_testcase_no_list.index(testcase)
            self.testscript["test"][index][testcase] = self.testcase_parser(
                testcase_list=self.testscript["test"][index][testcase],
                testcase_no=testcase,
            )

        # update script file
        self.yaml_dump(
            filepath=self.global_conf["script_filepath"], data=self.testscript
        )
