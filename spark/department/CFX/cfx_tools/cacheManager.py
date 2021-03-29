

import maya.cmds as cmds
import maya.mel as mel
import os, json
from os import listdir
from os.path import isfile, join

class CACHEMANAGER:

    def __init__(self):
        self.sim_cache_path, self.geo_cache_path, self.playblast_cache_path, self.final_cache_path = self.initcheck()

    def get_nucleus_start_frame(self):
        '''
        get the nucleus start frame  if there is no nucleus then it show you that start frame
        :return:
        '''

        nucleus = cmds.ls(type='nucleus')
        if nucleus:
            start_frame = cmds.getAttr(nucleus[0] + '.startFrame')
        else:
            start_frame = cmds.playbackOptions(q=True, minTime=True)

        return start_frame

    def ncloth_cache_def(self, replace=True, selected=False, sim_start_frame=0, sim_end_frame=100, notes=''):
        '''
        1 - get the atribute value
        2 - delete the exist cache if any
        3 - create a new cache if check checkbox say replace cache
        4 - save json file to the directory with the information


        :return:
        '''
        if selected:
            sel_ncloth_nodes = cmds.ls(sl=True)
        else:
            sel_ncloth_nodes = cmds.ls(type='nCloth')


        if not sel_ncloth_nodes:
            raise Exception('Please Select atlease nCloth transform or nCloth Shape node to run the command')

        new_transform_list = []
        for each in sel_ncloth_nodes:
            #if selected object is ncloth shape node
            if cmds.objectType(each) == 'nCloth':
                new_transform_list.append(cmds.listRelatives(each, p=True)[0])

            elif cmds.objectType(each) == 'transform':
                if cmds.objectType(cmds.listRelatives(each, s=True)[0]) == 'nCloth':
                    new_transform_list.append(each)
                else:
                    raise Exception('i have Found some of the other Transform node than nCloth please do only Select nCloth transofrm or shape Node')

            else:
                raise Exception('i Found Some of the other Shape node than nCloth Please only Select nCloth Shape node or Transform Node')

        #get the attr_val and put in the list
        attr_list_val = self.get_ncloth_nRigit_nConstraint_nHair_value()

        attr_list_val['Notes'] = notes

        #DELETE EXISTING CAHCE IF ANY

        cmds.select(new_transform_list)
        try:
            mel.eval('deleteCacheFile 2 { "keep", "" } ;')
        except:
            pass


        #SET THE WORK DIRECTORY AND SAVE THE CACHE IN THAT SO WE CAN QUERY FROMT HERE



        current_start_frame, current_end_frame = self.set_frames(new_start_frame=sim_start_frame,
                                                                 new_end_frame=sim_end_frame)

        ncloth_folder_name = self.sim_cache_path
        onlyfiles = [f for f in listdir(ncloth_folder_name) if isfile(join(ncloth_folder_name, f))]
        file_path_list = []

        for each in onlyfiles:
            if 'mc' in each:
                if self.get_file_name() in each:
                    file_path_list.append(each)
        file_name = self.get_file_name() + '_' + str(len(file_path_list))
        if '-' in file_name:
            file_name = file_name.replace('-', '_')
        cache_file_name = mel.eval('doCreateNclothCache 4 { "2", "1", "10", "OneFile", "1", "%s","0","%s","1", "add", "0", "1", "1","0","1" };' % (ncloth_folder_name, file_name))[0]


        print('this is the attr_val: ', attr_list_val)
        #write the file
        print(cache_file_name)
        json_path = ncloth_folder_name + '/' + cache_file_name.split('/')[-1].split('.')[0] + '.json'
        with open(json_path, 'w') as f:
            json.dump(attr_list_val, f)

        cmds.playbackOptions(minTime=current_start_frame, maxTime=current_end_frame)


        print('Cache is going to generate')


    def get_ncloth_nRigit_nConstraint_nHair_value(self):
        '''
        get all the Cloth nRigit nConstraint nHair value
        :return:
        '''
        #GET THE CLOTH VALUE
        attr_list = {}
        attr_list['nCloth'] = self.get_nCloth_val()
        attr_list['nRigid'] = self.get_nRigit_val()
        attr_list['dynamicConstraint'] = self.get_nConstraint_val()
        attr_list['hairSystem'] = self.get_hairSystem_val()
        attr_list['follicle'] = self.get_follicle_val()

        return attr_list





        pass

    def get_nCloth_val(self):
        '''
        get all the nCloth Value
        :return:
        '''
        ncloth_list = cmds.ls(type='nCloth')
        attr_list_val = {}

        for each_cloth in ncloth_list:
            attr_list_val[each_cloth] = {}
            for each_list in cmds.listAttr(each_cloth, v=True, k=True):
                try:
                    val = cmds.getAttr(each_cloth + '.' + each_list)
                    attr_list_val[each_cloth][each_list] = val
                except:
                    pass

        return attr_list_val

    def get_nRigit_val(self):
        '''
        get all the nCloth Value
        :return:
        '''
        ncloth_list = cmds.ls(type='nRigid')
        attr_list_val = {}

        for each_cloth in ncloth_list:
            attr_list_val[each_cloth] = {}
            for each_list in cmds.listAttr(each_cloth, v=True, k=True):
                try:
                    val = cmds.getAttr(each_cloth + '.' + each_list)
                    attr_list_val[each_cloth][each_list] = val
                except:
                    pass

        return attr_list_val

    def get_nConstraint_val(self):
        '''
        get all the nCloth Value
        :return:
        '''
        ncloth_list = cmds.ls(type='dynamicConstraint')
        attr_list_val = {}

        for each_cloth in ncloth_list:
            attr_list_val[each_cloth] = {}
            for each_list in cmds.listAttr(each_cloth, v=True, k=True):
                try:
                    val = cmds.getAttr(each_cloth + '.' + each_list)
                    attr_list_val[each_cloth][each_list] = val
                except:
                    pass

        return attr_list_val

    def get_hairSystem_val(self):
        '''
        get all the nCloth Value
        :return:
        '''
        ncloth_list = cmds.ls(type='hairSystem')
        attr_list_val = {}

        for each_cloth in ncloth_list:
            attr_list_val[each_cloth] = {}
            for each_list in cmds.listAttr(each_cloth, v=True, k=True):
                try:
                    val = cmds.getAttr(each_cloth + '.' + each_list)
                    attr_list_val[each_cloth][each_list] = val
                except:
                    pass

        return attr_list_val

    def get_follicle_val(self):
        '''
        get all the nCloth Value
        :return:
        '''
        ncloth_list = cmds.ls(type='follicle')
        attr_list_val = {}

        for each_cloth in ncloth_list:
            attr_list_val[each_cloth] = {}
            for each_list in cmds.listAttr(each_cloth, v=True, k=True):
                try:
                    val = cmds.getAttr(each_cloth + '.' + each_list)
                    attr_list_val[each_cloth][each_list] = val
                except:
                    pass

        return attr_list_val

    def set_frames(self, new_start_frame, new_end_frame):
        '''
        set the start and end frame temp
        :param new_start_frame:
        :param new_end_frame:
        :return:
        '''

        #GET CURRENT START AND END FRAME
        current_start_frame = cmds.playbackOptions(q=True, minTime=True)
        current_end_frame = cmds.playbackOptions(q=True, maxTime=True)

        cmds.playbackOptions(minTime=new_start_frame, maxTime=new_end_frame)

        return current_start_frame, current_end_frame

    def delete_ncloth_cache(self, selected=True):
        '''

        :param selected:
        :return:
        '''

        if selected:
            sel_ncloth_nodes = cmds.ls(sl=True)
        else:
            sel_ncloth_nodes = cmds.ls(type='nCloth')

        if not sel_ncloth_nodes:
            raise Exception('Please Select atlease nCloth transform or nCloth Shape node to run the command')

        new_transform_list = []
        for each in sel_ncloth_nodes:
            #if selected object is ncloth shape node
            if cmds.objectType(each) == 'nCloth':
                new_transform_list.append(cmds.listRelatives(each, p=True)[0])

            elif cmds.objectType(each) == 'transform':
                if cmds.objectType(cmds.listRelatives(each, s=True)[0]) == 'nCloth':
                    new_transform_list.append(each)
                else:
                    raise Exception('i have Found some of the other Transform node than nCloth please do only Select nCloth transofrm or shape Node')

            else:
                raise Exception('i Found Some of the other Shape node than nCloth Please only Select nCloth Shape node or Transform Node')

        cmds.select(new_transform_list)
        try:
            mel.eval('deleteCacheFile 2 { "keep", "" } ;')
        except:
            pass

    def get_file_name(self):
        '''

        :return:
        '''

        filepath = cmds.file(q=True, sn=True)
        if filepath == '':
            file_name = 'Untitle'
        else:
            file_name = os.path.basename(filepath).split('.')[0]

        return file_name

    def initcheck(self):
        '''
        THIS WILL HAPPEND BEFORE IT RUN THE UI PART
        :return:
        '''

        #GET THE FILE PATH
        filepath = cmds.file(q=True, sn=True)
        if filepath == '':
            filepath = cmds.workspace(q=True, dir=True)
        else:
            filepath = filepath.split(os.path.basename(filepath))[0]

        if filepath:
            #CHECK IF THE FOLDER IS EXISTS OR NOT
            sim_cache_dir = filepath + '/data/simCache'
            geo_cache_dir = filepath + '/data/geoCache'
            playblast_cache_dir = filepath + '/data/PlayBlast'
            final_cache_dir = filepath + '/data/FinalCache'

            if not os.path.exists(filepath + '/data'):
                os.mkdir(filepath + '/data')

            for each in [sim_cache_dir, geo_cache_dir, playblast_cache_dir, final_cache_dir]:
                if not os.path.exists(each):
                    os.mkdir(each)

            #GET THE SIM CACHE PATH



            return sim_cache_dir, geo_cache_dir, playblast_cache_dir, final_cache_dir



