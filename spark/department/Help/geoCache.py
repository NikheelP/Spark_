import maya.cmds as cmds
import maya.mel as mel
import os


class GEOCACHE:

    def __init__(self):
        pass

    def loadAbcImportPlugin(self):
        '''
        Load AbcImport plugin
        '''
        # Load AbcImport plugin
        if not cmds.pluginInfo('AbcImport', q=True, l=True):
            try:
                cmds.loadPlugin('AbcImport', quiet=True)
            except:
                raise Exception('Error loading AbcImport plugin!')

    def loadAbcExportPlugin(self):
        '''
        Load AbcExport plugin
        '''
        # Load AbcExport plugin
        if not cmds.pluginInfo('AbcExport', q=True, l=True):
            try:
                cmds.loadPlugin('AbcExport', quiet=True)
            except:
                raise Exception('Error loading AbcExport plugin!')

    def loadGpuCachePlugin(self):
        '''
        Load gpuCache plugin
        '''
        # Load gpuCache plugin
        if not cmds.pluginInfo('gpuCache', q=True, l=True):
            try:
                cmds.loadPlugin('gpuCache', quiet=True)
            except:
                raise Exception('Error loading gpuCache plugin!')

    def loadIkaGpuCachePlugin(self):
        '''
        Load glGpuCache plugin
        '''
        # Load glGpuCache plugin
        if not cmds.pluginInfo('glGpuCache', q=True, l=True):
            try:
                cmds.loadPlugin('glGpuCache', quiet=True)
            except:
                raise Exception('Error loading glGpuCache plugin!')

    def importMCCache(self, geo, cacheFile):
        '''
        Import and connect geometry cache file to the specified geometry
        @param geo: Geometry to load cache to
        @type geo: str
        @param cacheFile: Geometry cache file path to load
        @type cacheFile: str
        '''
        # Check geo
        if not cmds.objExists(geo): raise Exception('Geometry "" does not exist!')

        # Check file
        if not os.path.isfile(cacheFile): raise Exception('Cache file "' + cacheFile + '" does not exist!')

        # Load cache
        mel.eval('doImportCacheFile "' + cacheFile + '" "" {"' + geo + '"} {}')

    def importMCCacheList(self, geoList, cachePath, cacheFileList=[]):
        '''
        Import and connect geometry cache files from a specified path to the input geometry list
        @param geoList: List of geometry to load cache onto
        @type geoList: list
        @param cachePath: Directory path to load cache files from
        @type cachePath: str
        @param cacheFileList: List of cacheFiles to load. If empty, use geometry shape names. Optional.
        @type cacheFileList: list
        '''
        # Check source directory path
        if not os.path.isdir(cachePath):
            raise Exception('Cache path "' + cachePath + '" does not exist!')
        if not cachePath.endswith('/'): cachePath = cachePath + '/'

        # Check cacheFile list
        if cacheFileList and not (len(cacheFileList) == len(geoList)):
            raise Exception('Cache file and geometry list mis-match!')

        # For each geometry in list
        for i in range(len(geoList)):

            # Check geo
            if not cmds.objExists(geoList[i]):
                raise Exception('Geometry "' + geoList[i] + '" does not exist!')

            # Determine cache file
            if cacheFileList:
                cacheFile = cacheFile = cachePath + cacheFileList[i] + '.mc'
            else:
                # Get geometry shape
                shapeList = cmds.listRelatives(geoList[i], s=True, ni=True, pa=True)
                if not shapeList: raise Exception('No valid shape found for geometry!')
                geoShape = shapeList[0]
                cacheFile = cachePath + geoShape + '.mc'

            # Check file
            if not os.path.isfile(cacheFile):
                raise Exception('Cache file "' + cacheFile + '" does not exist!')

            # Import cache
            self.importMCCache(geoList[i], cacheFile)

    def exportMCCache(self, geo, cacheFile, cache_name, startFrame=1.0, endFrame=100.0, useTimeline=True, filePerFrame=False,
                      cachePerGeo=True, forceExport=False):
        '''
        @param geo: List of geometry to cache
        @type geo: list
        @param cacheFile: Output file name
        @type cacheFile: str
        @param startFrame: Start frame for cache output
        @type startFrame: float
        @param endFrame: End frame for cache output
        @type endFrame: float
        @param useTimeline: Get start and end from from the timeline
        @type useTimeline: bool
        @param filePerFrame: Write file per frame or single file
        @type filePerFrame: bool
        @param cachePerGeo: Write file per shape or single file
        @type cachePerGeo: bool
        @param forceExport: Force export even if it overwrites existing files
        @type forceExport: bool
        '''
        # Constant value args
        version = 5  # 2010
        refresh = 1  # Refresh during caching
        usePrefix = 0  # Name as prefix
        cacheAction = 'export'  # Cache action "add", "replace", "merge", "mergeDelete" or "export"
        simRate = 1  # Sim frame rate (steps per frame - ?)

        # Frame range
        if useTimeline:
            startFrame = cmds.playbackOptions(q=True, ast=True)
            endFrame = cmds.playbackOptions(q=True, aet=True)

        # Cache file distribution
        if filePerFrame:
            cacheDist = 'OneFilePerFrame'
        else:
            cacheDist = 'OneFile'

        # Determine destination directory and file
        fileName = cacheFile.split('/')[-1]
        cacheDir = cacheFile
        baseName = cache_name

        # Export cache
        cmds.select(geo)
        cache_path = 'doCreateGeometryCache ' + str(version) + ' {"0","' + str(startFrame) + '","' + str(
            endFrame) + '","' + cacheDist + '","' + str(refresh) + '","' + cacheDir + '","' + str(
            int(cachePerGeo)) + '","' + baseName + '","' + str(usePrefix) + '","' + cacheAction + '","' + str(
            int(forceExport)) + '","1","1","0","0","mcc" };'


        cache_path = 'doCreateGeometryCache "%s" {"2", "%s", "%s", "OneFile", "1", "%s", ' \
                     '"0", "%s", "0", "export", "0", "1", "1", "0", "1", "mcx", "0" }' %(str(version), str(startFrame), str(endFrame), cacheDir, baseName)

        print('this is the cacha path: ', cache_path)
        mel.eval(cache_path)
        '''
        mel.eval('doCreateGeometryCache ' + str(version) + ' {"0","' + str(startFrame) + '","' + str(
            endFrame) + '","' + cacheDist + '","' + str(refresh) + '","' + cacheDir + '","' + str(
            int(cachePerGeo)) + '","' + baseName + '","' + str(usePrefix) + '","' + cacheAction + '","' + str(
            int(forceExport)) + '","1","1","0","0","mcc" };')
        '''


    def export_abc_file(self,start_frame, end_frame, char_list, abc_file_path):
        '''

        :return:
        '''
        start = start_frame
        end = end_frame
        root = ''
        for each in char_list:
            root += ' -root ' + each

        save_name = abc_file_path

        command = "-frameRange " + str(start) + " " + str(end) + " -uvWrite -worldSpace " + root + " -file " + save_name
        cmds.AbcExport(j=command)