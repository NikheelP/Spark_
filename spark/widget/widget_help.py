import string
import traceback

import maya.cmds as cmds

class WIDGET_HELP():

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def get_punctuation(self, sentence):
        '''
        GET ALL THE punctuation FROM THE SENETENCE
        :return:
        '''
        sentence_list  = []
        for i in sentence:

            # checking whether the char is punctuation.
            if i in string.punctuation:
                sentence_list.append(i)


        return sentence_list


    def make_simple_text(self, sentence):
        '''
        ADD ALL THE _ IN THE punctuation AND SPACE
        :param sentence:
        :return:
        '''

        punctuation = self.get_punctuation(sentence)

        if punctuation:
            for each_punctuation in punctuation:
                if each_punctuation in sentence:
                    sentence = sentence.replace(each_punctuation, '_')

        if ' ' in sentence:
            sentence = sentence.replace(' ', '_')

        return sentence


    def listWidget_selection_change_select_obj(self, listWidget):
        '''

        :param listWidget:
        :return:
        '''

        getSelected = listWidget.selectedItems()
        obj = []
        if getSelected:
            a = 0
            for each in getSelected:
                baseNode = getSelected[a]
                getChildNode = baseNode.text(0)
                if cmds.objExists(getChildNode):
                    obj.append(getChildNode)
                a += 1
        if obj:
            cmds.select(obj)

    def dumpException(self, e=None):
        """
        Prints out an Exception message with a traceback to the console

        :param e: Exception to print out
        :type e: Exception
        """
        # print("%s EXCEPTION:" % e.__class__.__name__, e)
        # traceback.print_tb(e.__traceback__)
        traceback.print_exc()

