# Mega Man X8 WSX plugin by Zheneq (https://github.com/Zheneq/Noesis-Plugins)
# Modified by RainfallPianist
#   *
# Made for Noesis 4.428
from __future__ import annotations

import inc_noesis
from inc_noesis import *

import noesis
import rapi
import os
from collections import OrderedDict
from fmt_mmx8_wpg import WPGFile

BLOCK_HEADER_SIZE = 60


# registerNoesisTypes is called by Noesis to allow the script to register formats.
def registerNoesisTypes():
    handle = noesis.register("Mega Man X8 Model", ".wsx")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadModel(handle, noepyLoadModel)
    # noesis.setHandlerWriteModel(handle, noepyWriteModel)

    noesis.logPopup()
    return 1


def noepyCheckType(data):
    wsx = WSXFile(NoeBitStream(data))
    return wsx.checkType()


def noepyLoadModel(data, model_list):
    if noesis.NOESIS_PLUGINAPI_VERSION < 73:
        noesis.messagePrompt("This plugin requires Noesis v4.2 or higher.")
        return 0
    wsx = WSXFile(NoeBitStream(data))
    return wsx.load(model_list)


# def noepyWriteModel(model, bs):
#     meshesToExport = model.meshes

#     for mesh in meshesToExport:
#         print(mesh.name)


def parse_string(bs: inc_noesis.NoeBitStream, n_bytes):
    return bs.readBytes(n_bytes).decode("ascii").split("\0")[0]


def readQuat(bs: inc_noesis.NoeBitStream):
    r = NoeAngles.fromBytes(bs.readBytes(12))
    r[0], r[1], r[2] = -r[0], r[2], r[1]
    return r.toQuat()


class WSXFile:
    def __init__(self, bs):
        self.bs: inc_noesis.NoeBitStream = bs
        self.blockTypes = [
            "Skeletal mesh",
            "Static mesh",
            "UNKNWN (2)",
            "Animations",
            "Material",
            "Material animations [not parsed]",
            "UNKNWN (6)",
        ]
        self.blockHandlers = [
            self.parseBlockMesh,
            self.parseBlockMesh,
            self.parseUnknown,
            self.parseBlockAnim,
            self.parseBlockMat,
            lambda h: 0,
            lambda h: 0,
        ]

        self.valid = False

        self.objects = OrderedDict()

        # self.meshes = []

    def checkType(self):
        bs = self.bs
        bs.seek(0)

        self.valid = False

        print("Checking WSX file", bs.dataSize)
        if bs.dataSize < 8:
            return 0

        magic = parse_string(bs, 4)
        print(magic)

        p1 = bs.readInt()
        p2 = bs.readInt()
        FileSize = p1 + p2  # dataSize + shifts[0]

        print("File Size", hex(FileSize), hex(bs.dataSize), p1, p2, hex(p1), hex(p2))

        if FileSize != bs.dataSize:
            return 0

        self.valid = True
        return 1

    def load(self, model_list):
        # Check validity
        self.checkType()
        if not self.valid:
            return 0

        # Reset variables
        bs = self.bs
        bs.seek(0)

        # Header
        numRecords = bs.readInt()
        dataSize = bs.readInt()

        print("Loading {0} blocks ({1} bytes)".format(numRecords, dataSize))

        self.blockShifts = [bs.readInt() for i in range(numRecords)]
        fileSize = self.blockShifts[0] + dataSize
        self.blockShifts.append(fileSize)

        # Main loop
        for i in range(numRecords):
            # for i in range(8):
            self.parseBlock(i)

        # if matName is not None:
        #    wmesh.mesh.setMaterial(matName)

        # Sending to Noesis
        print("===== STATS =====")
        combined_textures = []
        combined_materials = []
        combined_meshes = []
        combined_bones = []
        combined_anims = []
        for obj in self.objects:
            mdl = NoeModel([], [], [])
            mdl.setMeshes(self.objects[obj].get("meshes", []))
            mdl.setBones(self.objects[obj].get("bones", []))
            mdl.setAnims(self.objects[obj].get("anims", []))
            mdl.setModelMaterials(
                NoeModelMaterials(
                    self.objects[obj].get("textures", []),
                    self.objects[obj].get("materials", []),
                )
            )
            mdl.name = obj
            model_list.append(mdl)

            combined_textures.extend(self.objects[obj].get("textures", []))
            combined_materials.extend(self.objects[obj].get("materials", []))
            combined_meshes.extend(self.objects[obj].get("meshes", []))
            combined_bones.extend(self.objects[obj].get("bones", []))
            combined_anims.extend(self.objects[obj].get("anims", []))

            # self.meshes.append(self.objects[obj].get('meshes', []))

            # print("{0}:".format(obj))
            # print("\tMeshes:    {0}".format(len(mdl.meshes)))
            # print("\tBones:     {0}".format(len(mdl.bones)))
            # print("\tAnims:     {0}".format(len(mdl.anims)))
            # print("\tTextures:  {0}".format(len(self.objects[obj].get('textures', []))))

        # mdl = NoeModel([], [], [])
        # mdl.setMeshes([TEST_MESH])
        # # mdl.setBones()
        # mdl.setModelMaterials(NoeModelMaterials(combined_textures, combined_materials))
        # mdl.name = "Combined"
        # model_list.append(mdl)

        mdl = NoeModel([], [], [])
        mdl.setMeshes(combined_meshes)
        # mdl.setBones(combined_bones)
        # mdl.setAnims(combined_anims)
        mdl.setModelMaterials(NoeModelMaterials(combined_textures, combined_materials))
        mdl.name = "Combined (v2)"
        model_list.append(mdl)

        return 1

    def parseBlock(self, idx):
        bs = self.bs

        bs.seek(self.blockShifts[idx], NOESEEK_ABS)

        # Magic Number
        magic = bs.readInt()
        if magic != 0x0101006C:
            print("bad record header", idx)
            return 0

        print(
            "*****************************************************************************",
            idx,
        )

        blockHeader = {
            "recordname": bs.readBytes(16).decode("ascii").split("\0")[0],
            "junk": bs.readInt(),
            "recordtype": bs.readInt(),
            "recordinfo": [bs.readInt(), bs.readInt(), bs.readInt()],
            "objectname": bs.readBytes(16).decode("ascii").split("\0")[0],
            "shift": self.blockShifts[idx],
        }

        # print(blockHeader)

        print(
            "{id:03}\t{blockname:<16}\t\t@ 0x{address:04X}\t(0x{size:X} bytes)\t({blocktype} for {objectname})".format(
                id=idx,
                blocktype=self.blockTypes[blockHeader["recordtype"]],
                blockname=blockHeader["recordname"],
                objectname=blockHeader["objectname"],
                address=blockHeader["shift"],
                size=self.blockShifts[idx + 1] - self.blockShifts[idx],
            )
        )

        # Create object if it does not exist
        if blockHeader["objectname"] not in self.objects:
            self.objects[blockHeader["objectname"]] = {}

        # Reset shift (all pointers inside a block are relative to this shift)
        bs.seek(self.blockShifts[idx], NOESEEK_ABS)

        isParsed = self.blockHandlers[blockHeader["recordtype"]](blockHeader)
        print("isParsed", isParsed)

    def parseUnknown(self, blockheader):
        bs = self.bs
        bs.seek(BLOCK_HEADER_SIZE, NOESEEK_REL)

        print([bs.readInt() for x in range(16)])

    def parseBlockMesh(self, blockHeader):
        bs = self.bs
        bs.seek(BLOCK_HEADER_SIZE, NOESEEK_REL)

        # todo: unknown data
        print(bs.readInt(), bs.readInt())

        # boneCount
        boneCount = bs.readShort()
        if boneCount == 0:
            return

        # todo: unknown data
        t = bs.readShort()
        print(t)

        shifts = {
            "bones": bs.readInt(),
            "junk": bs.readInt(),
            "s1": bs.readInt(),  # almost always boneCount * 64 bytes (almost == static/skeletal?)
            "s2": bs.readInt(),  # meshCount * 18 bytes
            "boneInfo": bs.readInt(),
            "s4": bs.readInt(),  # not always 0 bytes (int8)
            "junk": bs.readInt(),
            "m1": bs.readInt(),  # 32 bytes
            "meshInfo": bs.readInt(),
        }

        ################################## BONES ##################################
        # Reading bones
        bs.seek(blockHeader["shift"] + shifts["bones"], NOESEEK_ABS)
        bones = []
        for y in range(boneCount):
            p = {
                "rot": NoeAngles.fromBytes(bs.readBytes(12)),
                "trans": NoeVec3.fromBytes(bs.readBytes(12)),
                "scale": NoeVec3.fromBytes(bs.readBytes(12)),
            }
            p["rot"][0], p["rot"][1], p["rot"][2] = (
                -p["rot"][0],
                p["rot"][2],
                p["rot"][1],
            )
            bones.append(p)

        # Reading bone hierarchy
        bs.seek(blockHeader["shift"] + shifts["boneInfo"], NOESEEK_ABS)
        boneInfo = []
        for j in range(boneCount):
            t0 = [
                bs.readByte() for x in range(6)
            ]  # parent, 255 for 1st | 0 otherwise, bone index, ? some index , 0, 0

            boneInfo.append({"parent": t0[0], "index": t0[2], "other": t0[3]})

        # Building bones
        boneMatrices = []
        socketIndex = 0
        for j in range(boneCount):
            trans = NoeMat43().translate(bones[j]["trans"])
            rot = NoeMat43()
            scale = NoeMat43()

            if boneInfo[j]["parent"] != -1:
                rot = bones[boneInfo[j]["parent"]]["rot"].toMat43()
                scale = (
                    NoeVec3((bones[j]["scale"][0], 0.0, 0.0)),
                    NoeVec3((0.0, bones[j]["scale"][1], 0.0)),
                    NoeVec3((0.0, 0.0, bones[j]["scale"][2])),
                    NoeVec3((0.0, 0.0, 0.0)),
                )

            if boneInfo[j]["index"] != -1:
                boneInfo[j]["name"] = "bone{0:03}".format(boneInfo[j]["index"])
            else:
                boneInfo[j]["name"] = "socket{0:03}".format(socketIndex)
                socketIndex += 1

            bone = trans * scale * rot
            boneMatrices.append(bone)

        noeBones = [
            NoeBone(
                j,
                boneInfo[j]["name"],
                boneMatrices[j],
                parentIndex=boneInfo[j]["parent"],
            )
            for j in range(boneCount)
        ]

        noeBones = rapi.multiplyBones(noeBones)
        for j in range(boneCount):
            noeBones[j].setMatrix(bones[j]["rot"].toMat43() * noeBones[j].getMatrix())

        self.objects[blockHeader["objectname"]]["bones"] = noeBones

        ################################# MESHES ##################################
        bs.seek(blockHeader["shift"] + shifts["meshInfo"], NOESEEK_ABS)
        meshCount = bs.readInt()
        totalVertexCount = bs.readInt()

        # todo: unknown data
        # bs.seek(16, NOESEEK_REL)
        unknown = [bs.readByte() for x in range(16)]
        print("?", unknown)

        meshInfo = []
        meshBones = []
        for j in range(meshCount):
            meshInfo.append([bs.readInt() for k in range(8)])
            meshBones.append([bs.readShort() for k in range(32)])
        meshDataShift = bs.tell()

        # meshDataShift = blockHeader['shift'] + meshInfoShift + 24 + 96 * meshCount
        print("There are ", meshCount, " meshes")
        print("Mesh info", meshInfo)
        print("Shift", meshDataShift)
        self.objects[blockHeader["objectname"]]["meshes"] = []
        for j in range(meshCount):
            bs.seek(meshDataShift, NOESEEK_ABS)
            wmesh = WSXMesh(
                j,
                bs,
                boneInfo,
                meshInfo[j],
                meshBones[j],
                meshDataShift,
                blockHeader["recordtype"] == 0,
                blockHeader["objectname"] + "_" + str(j),
            )

            # todo: move this to mesh parser??
            matList = self.objects[blockHeader["objectname"]].get("materials", [])
            try:
                wmesh.mesh.setMaterial(matList[meshInfo[j][0]].name)
            except IndexError:
                print("Missing texture {0} for mesh {1}".format(meshInfo[j][0], j))
                print("Looking for", blockHeader["objectname"])

            try:
                TEST_MESH.setMaterial(matList[meshInfo[j][0]].name)
            except IndexError:
                print("Also for combined xd")

            self.objects[blockHeader["objectname"]]["meshes"].append(wmesh.mesh)

            # self.meshes.append(wmesh.mesh)
            # print(wmesh.mesh.sourceName)

        return 1

    def parseBlockAnim(self, blockHeader):
        bs = self.bs

        bs.seek(BLOCK_HEADER_SIZE, NOESEEK_REL)

        animsNum = bs.readInt()
        shift = bs.readInt()

        bs.seek(blockHeader["shift"] + shift)
        frameData = [
            {
                "fps": bs.readInt(),  # always 24?
                "frameCount": bs.readInt(),
                "boneCount": bs.readInt(),
                "junk": bs.readInt(),
                "animsInfoShift": bs.readInt(),
                "animsDataShift": bs.readInt(),
            }
            for x in range(animsNum)
        ]

        dataShifts = []
        for frame in frameData:
            bs.seek(blockHeader["shift"] + frame["animsInfoShift"])
            frame["animsInfo"] = [
                {
                    "framesCount": {
                        "rot": bs.readShort(),
                        "trans": bs.readShort(),
                        "scale": bs.readShort(),
                        "junk": bs.readShort(),
                    },
                    "framesRotShift": bs.readInt(),
                    "framesTransShift": bs.readInt(),
                    "framesScaleShift": bs.readInt(),
                }
                for x in range(frame["boneCount"])
            ]
            dataShifts.append(blockHeader["shift"] + frame["animsDataShift"])

            for bone in frame["animsInfo"]:
                bs.seek(
                    blockHeader["shift"]
                    + frame["animsDataShift"]
                    + bone["framesRotShift"]
                )
                bone["framesRot"] = [
                    NoeKeyFramedValue(bs.readInt(), readQuat(bs))
                    for x in range(bone["framesCount"]["rot"])
                ]

                bs.seek(
                    blockHeader["shift"]
                    + frame["animsDataShift"]
                    + bone["framesTransShift"]
                )
                bone["framesTrans"] = [
                    NoeKeyFramedValue(bs.readInt(), NoeVec3.fromBytes(bs.readBytes(12)))
                    for x in range(bone["framesCount"]["trans"])
                ]

                bs.seek(
                    blockHeader["shift"]
                    + frame["animsDataShift"]
                    + bone["framesScaleShift"]
                )
                bone["framesScale"] = [
                    NoeKeyFramedValue(bs.readInt(), NoeVec3.fromBytes(bs.readBytes(12)))
                    for x in range(bone["framesCount"]["scale"])
                ]

        anims = []
        for i in range(len(frameData)):
            frame = frameData[i]

            animName = "anim_{0:03}".format(i)
            # todo: bones are not always there??
            animBones = self.objects[blockHeader["objectname"]].get("bones", [])
            animFrameRate = 0.5  # float(frame["fps"])
            animNumFrames = frame["frameCount"]

            animKFBones = []

            if frame["boneCount"] != len(animBones):
                print("> Not parsed")
                continue

            for x in range(frame["boneCount"]):
                b = NoeKeyFramedBone(x)
                b.setRotation(frame["animsInfo"][x]["framesRot"])
                b.setTranslation(frame["animsInfo"][x]["framesTrans"])
                b.setScale(
                    frame["animsInfo"][x]["framesScale"], noesis.NOEKF_SCALE_VECTOR_3
                )

                animKFBones.append(b)

            anims.append(
                NoeKeyFramedAnim(animName, animBones, animKFBones, animFrameRate)
            )

        self.objects[blockHeader["objectname"]]["anims"] = anims
        return 1

    def parseBlockMat(self, blockHeader):
        bs = self.bs

        if "textures" not in self.objects[blockHeader["objectname"]]:
            self.objects[blockHeader["objectname"]]["textures"] = []
        if "materials" not in self.objects[blockHeader["objectname"]]:
            self.objects[blockHeader["objectname"]]["materials"] = []

        print(
            "ID",
            blockHeader["recordinfo"],
            "at addr",
            hex(bs.tell()),
            "shift",
            hex(blockHeader["shift"]),
            BLOCK_HEADER_SIZE,
        )
        print(blockHeader)
        if blockHeader["recordinfo"][0] == 0:
            texList = []
            matList = []
            materialData = {}

            bs.seek(BLOCK_HEADER_SIZE, NOESEEK_REL)

            materialData["count"] = bs.readInt()
            print(materialData["count"], "materials to discover")

            # todo: unknown data
            pos = bs.tell()
            unknown = [bs.readByte() for x in range(0x6C)]
            print("?", unknown, "at pos", hex(pos))
            bs.seek(pos, NOESEEK_ABS)

            pos = bs.tell()
            unknown = [bs.readInt() for x in range(0x6C // 2)]
            print("? (int)", unknown)
            bs.seek(pos, NOESEEK_ABS)

            bs.seek(blockHeader["shift"] + 0x6C, NOESEEK_ABS)

            # todo: recheck this
            TextureMapping = [
                {
                    "shift": bs.readInt() & 0xFFFFFF,
                    "size": bs.readInt() & 0xFFFFFF,
                }  # int24 lolwat?
                for x in range(materialData["count"])
            ]
            materialData["mapping"] = TextureMapping

            TextureStrings = [
                bs.readBytes(256).decode("ascii").split("\0", 1)[0] for x in range(4)
            ]  # [2] & [3] always empty
            print(TextureStrings)
            if TextureStrings[0] != "wsxwpg":
                print("\t\tWSXWPG magic code is wrong!")
                return 0

            # loading textures
            materialData["name"] = TextureStrings[1]
            dirPath = rapi.getDirForFilePath(rapi.getInputName())
            texPath = os.path.join(dirPath, "wpg", TextureStrings[1])
            # WPGFile(texList, blockHeader['objectname'], materialData['mapping'], texPath).load()
            wpg_file = WPGFile(texList, blockHeader["objectname"], None, texPath)
            wpg_file.load()
            print("Mapping", materialData["mapping"])

            for t in texList:
                matList.append(NoeMaterial(t.name, t.name))

            self.objects[blockHeader["objectname"]]["textures"].extend(texList)
            self.objects[blockHeader["objectname"]]["materials"].extend(matList)
            print("Loaded materials", len(matList), matList)
            print("Loaded textures", len(texList), texList)
            return 1
        elif blockHeader["recordinfo"][0] == -1:
            bs.seek(BLOCK_HEADER_SIZE, NOESEEK_REL)

            # print("Count?", bs.readInt())
            pattern = [bs.readInt() for i in range(12)]
            print("Pattern", pattern)
            if pattern == [0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                print("Pattern is correct, and we are at addr", hex(bs.tell()))

                # todo: not sure about this part
                # return 0
                # use legacy
                # crashes when this is the first block of the file
                items = list(self.objects.items())
                if len(items) == 1:
                    print("Items", items)
                    source = items[-1][1]
                    self.objects[blockHeader["objectname"]]["textures"].extend(
                        source["textures"]
                    )
                    self.objects[blockHeader["objectname"]]["materials"].extend(
                        source["materials"]
                    )
                    return 1

                elif len(items) >= 2:
                    # second_to_last = items[-2]
                    # print("Items", items, "second to last", second_to_last)
                    # if len(second_to_last) > 2:
                    source = items[-2][1]
                    print("Source", source)
                    print([bs.readInt() for i in range(32)])
                    self.objects[blockHeader["objectname"]]["textures"].extend(
                        source["textures"]
                    )
                    self.objects[blockHeader["objectname"]]["materials"].extend(
                        source["materials"]
                    )
                    return 1
        return 0

    def recombineNoesisMeshes(self, model):
        # meshesBySourceName = {}
        # for mesh in mdl.meshes:
        # 	meshesBySourceName[mesh.sourceName] = meshesBySourceName.get(mesh.sourceName) or []
        # 	meshesBySourceName[mesh.sourceName].append(mesh)
        combinedMeshes = []
        # for sourceName, meshList in meshesBySourceName.items():
        for meshList in self.meshes:
            newPositions = []
            newUV1 = []
            newUV2 = []
            newUV3 = []
            newTangents = []
            newWeights = []
            newIndices = []
            newColors = []
            for mesh in meshList:
                tempIndices = []
                for index in mesh.indices:
                    tempIndices.append(index + len(newPositions))
                newPositions.extend(mesh.positions)
                newUV1.extend(mesh.uvs)
                newUV2.extend(mesh.lmUVs)
                newUV3.extend(mesh.uvxList[0] if len(mesh.uvxList) > 0 else [])
                newColors.extend(mesh.colors)
                newTangents.extend(mesh.tangents)
                newWeights.extend(mesh.weights)
                newIndices.extend(tempIndices)

            combinedMesh = NoeMesh(
                newIndices,
                newPositions,
                meshList[0].sourceName,
                meshList[0].sourceName,
                model.globalVtx,
                model.globalIdx,
            )
            combinedMesh.setTangents(newTangents)
            combinedMesh.setWeights(newWeights)
            combinedMesh.setUVs(newUV1)
            combinedMesh.setUVs(newUV2, 1)
            combinedMesh.setUVs(newUV3, 2)
            combinedMesh.setColors(newColors)
            if len(combinedMesh.positions) > 65535:
                print(
                    "Warning: Mesh exceeds the maximum of 65535 vertices (has",
                    str(len(combinedMesh.positions)) + "):\n	",
                    combinedMesh.name,
                )
            else:
                combinedMeshes.append(combinedMesh)

        return combinedMeshes


TEST_MESH = NoeMesh([], [], "CombinedMesh")


class WSXMesh:
    def __init__(
        self,
        index,
        bs,
        boneInfo,
        meshInfo,
        meshBones,
        meshDataShift,
        bSkeletal,
        meshName,
    ):
        global TEST_MESH

        VertexLen = 9
        if bSkeletal:
            VertexLen = 15
        dcType = meshInfo[1]  # triangles / triangle strip
        vertexCount = meshInfo[2]
        dcShift = meshInfo[3] * 4 * VertexLen

        # print("\t\t\tMesh {0:02}, {1} vertices, type {2}".format(index, vertexCount, dcType))
        # print(meshInfo)
        # print("bones: ", meshBones)
        # break

        self.mesh = NoeMesh([], [], meshName)
        if dcType == 0:
            # TRIANGLES
            self.mesh.indices = [x for x in range(vertexCount)]
            TEST_MESH.indices.extend([x for x in range(vertexCount)])
        elif dcType == 1:
            # TRIANGLE_STRIP
            for x in range(0, vertexCount - 4, 2):
                self.mesh.indices.extend([x, x + 1, x + 2, x + 2, x + 1, x + 3])
                TEST_MESH.indices.extend([x, x + 1, x + 2, x + 2, x + 1, x + 3])
        else:
            print("=============================================")

        bs.seek(dcShift, NOESEEK_REL)

        for x in range(vertexCount):
            vertex = NoeVec3.fromBytes(bs.readBytes(12))
            self.mesh.positions.append(vertex)
            TEST_MESH.positions.append(vertex)

            normal = NoeVec3.fromBytes(bs.readBytes(12))
            self.mesh.normals.append(normal)
            TEST_MESH.normals.append(normal)

            uv = NoeVec3.fromBytes(bs.readBytes(12))
            self.mesh.uvs.append(uv)  # junk, u, v
            TEST_MESH.uvs.append(uv)

            self.mesh.uvs[-1][0], self.mesh.uvs[-1][1], self.mesh.uvs[-1][2] = (
                self.mesh.uvs[-1][1],
                self.mesh.uvs[-1][2],
                self.mesh.uvs[-1][0],
            )  # u, v, junk
            TEST_MESH.uvs[-1][0], TEST_MESH.uvs[-1][1], TEST_MESH.uvs[-1][2] = (
                TEST_MESH.uvs[-1][1],
                TEST_MESH.uvs[-1][2],
                TEST_MESH.uvs[-1][0],
            )  # u, v, junk
            if bSkeletal:
                boneWeights = [bs.readFloat() for y in range(3)]
                vertexColor = NoeVec3.fromBytes(bs.readBytes(12))

                boneIndices = []
                boneLocalIndices = [meshBones[int(y / 3) - 1] for y in vertexColor]
                for y in boneLocalIndices:
                    for z in range(len(boneInfo)):
                        if boneInfo[z]["index"] == y:
                            boneIndices.append(z)
                            break
                    else:
                        print("bone data is corrupt (bone {0} not found)".format(y))

                # print("boneWeights", boneWeights)
                # print("vertexColor", vertexColor)
                # print("vertexColorIdx", [int(y/3)-1 for y in vertexColor])
                # print("boneLocalIndices", boneLocalIndices)
                # print("boneIndices", boneIndices)
                # print()

                self.mesh.weights.append(NoeVertWeight(boneIndices, boneWeights))
                TEST_MESH.weights.append(NoeVertWeight(boneIndices, boneWeights))
            else:
                self.mesh.weights.append(NoeVertWeight([meshBones[0]], [1.0]))
                TEST_MESH.weights.append(NoeVertWeight([meshBones[0]], [1.0]))
