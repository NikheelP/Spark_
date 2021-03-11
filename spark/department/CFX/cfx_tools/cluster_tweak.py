
import maya.cmds as cmds

class CLUSTER_TWEAK:
    def __init__(self):
        pass

    def cluster_tweak(self):
        from spark.department.Rigging.rigging_tool import soft_selection_to_cluster
        reload(soft_selection_to_cluster)
        from spark.department.Rigging import SOFT_SELECTION_TO_CLUSTER
        soft_selection_to_cluster_class = SOFT_SELECTION_TO_CLUSTER()



        clusteer_handle_name = soft_selection_to_cluster_class.soft_selection_to_cluster()
        print(clusteer_handle_name)

        #Create a Rivet and do the process
        title = 'Need to update with the Rivet'
        message = 'add the rivet command do the configure to move with the object'
        cmds.confirmDialog(title=title, message=message, button=['OK'], defaultButton='Ok',
                           cancelButton='No', dismissString='No')