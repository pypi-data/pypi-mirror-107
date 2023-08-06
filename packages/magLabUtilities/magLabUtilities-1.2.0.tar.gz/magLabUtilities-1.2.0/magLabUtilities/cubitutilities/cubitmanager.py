#!python3

import subprocess
from typing import Tuple, List, Dict, Union
from magLabUtilities.parametrictestutilities.testmanager import TestCase

class GeometryGenerator:
    @staticmethod
    def fromScript(scriptFP:str, overrideParameterList:List[Tuple[str,Union[str,int,float]]]):
        cmdString = ''
        cmdList = []
        for overrideParameter in overrideParameterList:
            if isinstance(overrideParameter[1], str):
                cmdString += r'%s = \'%s\'\n' % (overrideParameter[0], overrideParameter[1])
                cmdList.append('%s = \'%s\'' % (overrideParameter[0], overrideParameter[1]))
            elif isinstance(overrideParameter[1], int):
                cmdString += r'%s = %d\n' % (overrideParameter[0], overrideParameter[1])
                cmdList.append('%s = %d' % (overrideParameter[0], overrideParameter[1]))
            elif isinstance(overrideParameter[1], float):
                cmdString += r'%s = %f\n' % (overrideParameter[0], overrideParameter[1])
                cmdList.append('%s = %f' % (overrideParameter[0], overrideParameter[1]))

        subprocess.run(['py', '-2', scriptFP, *cmdList])

    @staticmethod
    def fromTestCase(testCase:TestCase, processParameterList:List[str], scriptFP:str):
        overrideParameterList = []
        overrideParameterList.append(('unvFD', testCase.caseFD))
        for processParameter in processParameterList:
            coord = testCase.coordDict[processParameter]
            overrideParameterList.append((coord.name, coord.value))

        GeometryGenerator.fromScript(scriptFP, overrideParameterList)
