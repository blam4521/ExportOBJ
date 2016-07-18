import os, shutil
import os.path

#importing maya standalone
import maya
import maya.standalone
from maya import cmds as mc
#import pymel.core as pm

def export_obj(file_path):

	# Start Maya in batch mode
	maya.standalone.initialize( name='python' )

	# Load obj plugins
	mc.loadPlugin( "objExport" )

	# Initial directory
	files = os.listdir( file_path )
	
	# Path for creating new destination
	full_path =( file_path ) 
	
	# Create new path
	destination = os.path.join( full_path,"obj_files" )

	if not os.path.exists(destination):
		print "Making directory: ", destination
		make = os.makedirs(destination)

	# Find files that end with ma
	for mayafile in files:
		if mayafile.endswith( ".ma" ):
			
			# Open maya file
			mc.file( mayafile, force=True, open=True )
			
			# Iterate through the timeline
			totalNumFrames = int( mc.playbackOptions(q=True,maxTime=True) )

			
			for i in range( 1, totalNumFrames+1 ):
				mc.currentTime(i)
				print "the current frame is",i

				# Get all meshes in the scene
				meshes = mc.ls( type="mesh", long=False)
				for mesh in meshes:
					mc.select(mesh)
					saveFile = "%s.%04d" % (mesh, i) + ".obj"
					path = os.path.join( destination, saveFile )
					mc.file( path, type="OBJexport", pr=True, exportSelected=True )
					print "Saved %s"%saveFile
				print '\n'		


if __name__ == '__main__':
	response = raw_input("Please enter the file path: ")
	export_obj(response)
	print "...File is Done Saving"
