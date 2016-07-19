import os, shutil
import os.path
import sys

#importing maya standalone
import maya
import maya.standalone
from maya import cmds as mc
#import pymel.core as pm

## ----------------------------------------------------------------------

def export_obj(file_name, destination):
	

	#print file_path
	#print("exporting")
	#return True

	# Start Maya in batch mode
	maya.standalone.initialize( name='python' )

	# Load obj plugins
	mc.loadPlugin( "objExport" )

	# Open maya file
	mc.file( file_name, force=True, open=True )
	
	# Iterate through the timeline
	end_frame = int( mc.playbackOptions(q=True,maxTime=True) )
	begin_frame = int( mc.playbackOptions(q=True,minTime=True) )
	
	
	for i in range( begin_frame, end_frame+1 ):
		mc.currentTime(i)
		print "the current frame is",i

		# Get all meshes in the scene, filter through it 
		
		for mesh in mc.ls( type="mesh", long=False, io=False, v=True, tex=False, set=False, mat=False ):
			mc.select(mesh)
			saveFile = "%s.%04d" % (mesh, i) + ".obj"
			path = os.path.join( destination, saveFile )
			
			# Check to see if file exists
			if mc.file( path, q=True, exists=True ):
				print("Skipping %s-- already exists."%path)
			else:
				mc.file( path, type="OBJexport", pr=True, exportSelected=True )
				print "Saved %s"%saveFile
		print '\n'	

## ----------------------------------------------------------------------

def main(full_path):

	# Initial directory
	files = os.listdir( full_path )
	
	# Path for creating new destination
	full_path = ( full_path ) 
	
	# Create new path
	destination = os.path.join( full_path,"obj_files" )


	if not os.path.exists(destination):
		print("Making directory: ", destination)
		make = os.makedirs(destination)
		#[mayafile for mayafile in files if mayafile.endswith( ".ma" ) export_obj( full_path )]
		#if os.path.exists(variants):
		#	print(" %s -- already exists."% variants)
		#else:
		# Find files that end with ma
	else:
		print("Directory already exists: ", destination)
		
	for mayafile in files:
		if mayafile.endswith( ".ma" ):
			export_obj( mayafile, destination )
	
## ----------------------------------------------------------------------

if __name__ == '__main__':
	main(sys.argv[1])