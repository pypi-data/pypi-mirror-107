#!python3

from typing import List, Dict, Union, Callable
import subprocess
from magLabUtilities.parametrictestutilities.testmanager import TestCase
from magLabUtilities.fileutilities.common import replaceTagsInTxt

class MagstromSimulation:
    @staticmethod
    def inputFileFromTemplate(inputFileTemplateFP:str, inputFileFP:str, replacementDict:Dict) -> None:
        replaceTagsInTxt(inputFileTemplateFP, inputFileFP, replacementDict)

    @staticmethod
    def runFromTestCase(testCase:TestCase, processParameterList:List[str], magstromExeFP:str) -> None:
        subprocess.run([magstromExeFP, testCase.processDataDict['inputFileFP']])

class LinearMagstromSimulation(MagstromSimulation):
    @staticmethod
    # TODO replacementDict:Dict[str, Union[str, Callable[[TestCase], str]]]
    def fromTestCase(testCase:TestCase, 
                    processParameterList:List[str],
                    inputFileTemplateFP:str,
                    inputFileFN:str=None, # If None, testCase.name used.
                    outputFD:str=None, # If None, testCase.caseFD used.
                    jobName:str=None, # If None, testCase.name used.
                    replacementDict:Dict[str,str]={} # Additional replacements for input file
                    ) -> None:

        if inputFileFN is None:
            inputFileFP = testCase.caseFD + testCase.name + '.txt'
        if outputFD is None:
            replacementDict['__outputFD__'] = testCase.caseFD
        if jobName is None:
            replacementDict['__jobName__'] = testCase.name

        for processParameter in processParameterList:
            coord = testCase.coordDict[processParameter]
            replacementDict['__%s__' % coord.name] = str(coord.value)

        LinearMagstromSimulation.inputFileFromTemplate(inputFileTemplateFP, inputFileFP, replacementDict)

        testCase.processDataDict['inputFileFP'] = inputFileFP
