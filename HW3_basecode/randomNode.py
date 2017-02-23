# Reference: http://download.autodesk.com/us/maya/2009help/API/circle_node_8py-example.html

# randomNode.py
#   Produces random locations to be used with the Maya instancer node.

import sys
import random
import LSystem
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

# Useful functions for declaring attributes as inputs or outputs.
def MAKE_INPUT(attr):
    attr.setKeyable(True)
    attr.setStorable(True)
    attr.setReadable(True)
    attr.setWritable(True)
def MAKE_OUTPUT(attr):
    attr.setKeyable(False)
    attr.setStorable(False)
    attr.setReadable(True)
    attr.setWritable(False)


# === randomNode part===
# ======================
# Define the name of the node
kPluginRandomNodeTypeName = "randomNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
randomNodeId = OpenMaya.MTypeId(0x8704)

# Node definition
class randomNode(OpenMayaMPx.MPxNode):
    # Declare class variables:
    # TODO:: declare the input and output class variables
    #         i.e. inNumPoints = OpenMaya.MObject()
    
    # constructor
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    inNumPoints = OpenMaya.MObject()
    outPoints = OpenMaya.MObject()

    minX = OpenMaya.MObject()
    minY = OpenMaya.MObject()
    minZ = OpenMaya.MObject()
    minVector = OpenMaya.MObject()
    maxX = OpenMaya.MObject()
    maxY = OpenMaya.MObject()
    maxZ = OpenMaya.MObject()
    maxVector = OpenMaya.MObject()

    # compute
    def compute(self,plug,data):
        # TODO:: create the main functionality of the node. Your node should 
        #         take in three floats for max position (X,Y,Z), three floats 
        #         for min position (X,Y,Z), and the number of random points to
        #         be generated. Your node should output an MFnArrayAttrsData 
        #         object containing the random points. Consult the homework
        #         sheet for how to deal with creating the MFnArrayAttrsData. 
        if plug == randomNode.outPoints:
            # read the # of random points to be generated
            inNumPointsData = data.inputValue(randomNode.inNumPoints)
            inNumPointsValue = inNumPointsData.asFloat()
            # read minimum bound
            minVectorData = data.inputValue(randomNode.minVector)
            minVectorData = minVectorData.asFloat3()
            # read maximum bound
            maxVectorData = data.inputValue(randomNode.maxVector)
            maxVectorData = maxVectorData.asFloat3()
            
            # Output value
            pointsData = data.outputValue(randomNode.outPoints) #the MDataHandle
            pointsAAD = OpenMaya.MFnArrayAttrsData() #the MFnArrayAttrsData
            pointsObject = pointsAAD.create() #the MObject
            
            # Create the vectors for position and id
            positionArray = pointsAAD.vectorArray("position")
            idArray = pointsAAD.doubleArray("id")
            
            # DONE:: Loop to fill the arrays: 
            for num in range(0, int(inNumPointsValue)):
                startx = random.uniform(minVectorData[0], maxVectorData[0])
                starty = random.uniform(minVectorData[1], maxVectorData[1])
                startz = random.uniform(minVectorData[2], maxVectorData[2])
                
                positionArray.append(OpenMaya.MVector(startx, starty, startz))
                idArray.append(num) 
            
            # Finally set the output data handle 
            pointsData.setMObject(pointsObject) 


        data.setClean(plug)
    
# initializer
def randomNodeInitializer():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    # TODO:: initialize the input and output attributes. Be sure to use the 
    #         MAKE_INPUT and MAKE_OUTPUT functions.
    randomNode.inNumPoints = nAttr.create("numPoints", "n", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.minX = nAttr.create("minX", "miX", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.minY = nAttr.create("minY", "miY", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.minZ = nAttr.create("minZ", "miZ", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.minVector = nAttr.create("minVector", "miV", randomNode.minX, randomNode.minY, randomNode.minZ)
    MAKE_INPUT(nAttr)
    randomNode.maxX = nAttr.create("maxX", "maX", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.maxY = nAttr.create("maxY", "maY", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.maxZ = nAttr.create("maxZ", "maZ", OpenMaya.MFnNumericData.kFloat, 0.0)
    MAKE_INPUT(nAttr)
    randomNode.maxVector = nAttr.create("maxVector", "maV", randomNode.maxX, randomNode.maxY, randomNode.maxZ)
    MAKE_INPUT(nAttr)
    # Output attributes
    randomNode.outPoints = tAttr.create("outPoints", "op", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    MAKE_OUTPUT(tAttr)

    try:
        # TODO:: add the attributes to the node and set up the
        #         attributeAffects (addAttribute, and attributeAffects)
        print "Initialization!\n"

        # Add attributes
        randomNode.addAttribute(randomNode.inNumPoints)
        randomNode.addAttribute(randomNode.minVector)
        randomNode.addAttribute(randomNode.maxVector)
        randomNode.addAttribute(randomNode.outPoints)    
        
        # Set attributeAffects
        randomNode.attributeAffects(randomNode.inNumPoints, randomNode.outPoints)
        randomNode.attributeAffects(randomNode.minVector, randomNode.outPoints)
        randomNode.attributeAffects(randomNode.maxVector, randomNode.outPoints)   

    except:
        sys.stderr.write( ("Failed to create attributes of %s node\n", kPluginRandomNodeTypeName) )

# creator
def randomNodeCreator():
    return OpenMayaMPx.asMPxPtr( randomNode() )




# === Instancer part===
# ======================

# Define the name of the node
kPluginLSystemInstanceNodeTypeName = "LSystemInstanceNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
LSystemInstanceNodeId = OpenMaya.MTypeId(0x261)

# Node definition
class LSystemInstanceNode(OpenMayaMPx.MPxNode):
    # Declare class variables
    angle = OpenMaya.MObject()
    stepSize = OpenMaya.MObject()
    grammarFile = OpenMaya.MObject()
    iterations = OpenMaya.MObject()
    outputBranches = OpenMaya.MObject()
    outputFlowers = OpenMaya.MObject()
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self,plug,data):
        print "LSystemInstanceNode compute\n"
        
        # Retrieve input values
        angleData = data.inputValue(LSystemInstanceNode.angle)
        angleValue = angleData.asDouble()
        
        stepSizeData = data.inputValue(LSystemInstanceNode.stepSize)
        stepSizeValue = stepSizeData.asDouble()
        
        grammarFileData = data.inputValue(LSystemInstanceNode.grammarFile)
        grammarFileValue = grammarFileData.asString()
        
        iterationsData = data.inputValue(LSystemInstanceNode.iterations)
        iterationsValue = iterationsData.asDouble()
        
        # Output values
        outBranchesData = data.outputValue(LSystemInstanceNode.outputBranches) #the MDataHandle
        outBranchesAAD = OpenMaya.MFnArrayAttrsData() #the MFnArrayAttrsData
        outBranchesObject = outBranchesAAD.create() #the MObject
        
        outFlowersData = data.outputValue(LSystemInstanceNode.outputFlowers)
        outFlowersAAD = OpenMaya.MFnArrayAttrsData()
        outFlowersObject = outFlowersAAD.create()
        
        # Create the vectors for Branches
        positionArrayBranch = outBranchesAAD.vectorArray("position")
        idArrayBranch = outBranchesAAD.doubleArray("id")
        scaleArrayBranch = outBranchesAAD.vectorArray("scale")
        aimDirArrayBranch = outBranchesAAD.vectorArray("aimDirection")
        
        # Create the vectors for Flowers
        positionArrayFlower = outFlowersAAD.vectorArray("position")
        idArrayFlower = outFlowersAAD.doubleArray("id")
        scaleArrayFlower = outFlowersAAD.vectorArray("scale")
        aimDirArrayFlower = outFlowersAAD.vectorArray("aimDirection")
        

        system = LSystem.LSystem()
        system.loadProgramFromString(str(grammarFileValue))
        system.setDefaultAngle(angleValue)
        system.setDefaultStep(stepSizeValue)
        
        branches = LSystem.VectorPyBranch()
        flowers = LSystem.VectorPyBranch()
                
		# Run Grammar String
        for i in range (0, int(iterationsValue)):
            system.processPy(i, branches, flowers)
              
        for idx, branch in enumerate(branches):
            startPos = OpenMaya.MVector(branch[0], branch[2], branch[1]) 
            endPos = OpenMaya.MVector(branch[3], branch[5], branch[4])
            dir = endPos - startPos 
            positionArrayBranch.append(endPos)
            idArrayBranch.append(idx)
            scaleArrayBranch.append(OpenMaya.MVector(1,1,1))
            aimDirArrayBranch.append(dir)         
        
        for idx, flower in enumerate(flowers):
            pos = OpenMaya.MVector(flower[0], flower[2], flower[1])
            positionArrayFlower.append(pos)
            idArrayFlower.append(idx)
            scaleArrayFlower.append(OpenMaya.MVector(1,1,1))
            aimDirArrayFlower.append(OpenMaya.MVector(1,1,1))
        
        outBranchesData.setMObject(outBranchesObject)
        outFlowersData.setMObject(outFlowersObject)

        data.setClean(plug)

# initializer
def LSystemInstanceNodeInitializer():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()
    
    # Input
    LSystemInstanceNode.angle = nAttr.create("angle", "a", OpenMaya.MFnNumericData.kDouble, 30.0)
    MAKE_INPUT(nAttr)
    LSystemInstanceNode.stepSize = nAttr.create("stepSize", "ss", OpenMaya.MFnNumericData.kDouble, 5.0)
    MAKE_INPUT(nAttr)
    LSystemInstanceNode.grammarFile = tAttr.create("grammarFile", "g", OpenMaya.MFnData.kString)
    MAKE_INPUT(nAttr)
    LSystemInstanceNode.iterations = nAttr.create("iterations", "i", OpenMaya.MFnNumericData.kDouble, 5.0)
    MAKE_INPUT(nAttr)
    # Output
    LSystemInstanceNode.outputBranches = tAttr.create("outputBranches", "ob", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    MAKE_OUTPUT(tAttr)
    LSystemInstanceNode.outputFlowers = tAttr.create("outputFlowers", "of", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    MAKE_OUTPUT(tAttr)
    
    try:
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.angle)
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.stepSize)
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.grammarFile)
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.iterations)
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.outputBranches)        
        LSystemInstanceNode.addAttribute(LSystemInstanceNode.outputFlowers)        
        
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.angle,LSystemInstanceNode.outputBranches)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.angle,LSystemInstanceNode.outputFlowers)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.stepSize,LSystemInstanceNode.outputBranches)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.stepSize,LSystemInstanceNode.outputFlowers)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.grammarFile,LSystemInstanceNode.outputBranches)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.grammarFile,LSystemInstanceNode.outputFlowers)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.iterations,LSystemInstanceNode.outputBranches)
        LSystemInstanceNode.attributeAffects(LSystemInstanceNode.iterations,LSystemInstanceNode.outputFlowers)
        
    except:
        sys.stderr.write( ("Failed to create attributes of %s node\n", kPluginLSystemInstanceNodeTypeName) )
        
        
# creator
def LSystemInstanceNodeCreator():
    return OpenMayaMPx.asMPxPtr( LSystemInstanceNode() )
    

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginRandomNodeTypeName, randomNodeId, randomNodeCreator, randomNodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginRandomNodeTypeName )

    try:
        mplugin.registerNode( kPluginLSystemInstanceNodeTypeName, LSystemInstanceNodeId, LSystemInstanceNodeCreator, LSystemInstanceNodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginLSystemInstanceNodeTypeName )


# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( randomNodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginRandomNodeTypeName )
    try:
        mplugin.deregisterNode( LSystemInstanceNodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginLSystemInstanceNodeTypeName )


def createPyUI():
    OpenMaya.MGlobal.executeCommand("createLSystemUI")
    
def deletePyUI():
    OpenMaya.MGlobal.executeCommand("deleteLSystemUI") 