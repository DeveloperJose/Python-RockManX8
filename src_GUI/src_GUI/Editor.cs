using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Memory;
namespace src_GUI
{
    public class Editor
    {
        public static Mem M = new Mem();

        public Vec3 Player1Vec = new Vec3(M.GetCode("NOCD.exe+0x041A61F8"));

        private bool ActiveEnemies
        {
            get { return Editor.M.ReadInt("0x0428DB88") == 0; }
            set { Editor.M.WriteMemory("0x0428DB88", "int", value ? "0" : "1"); }
        }
        private bool ActiveWind
        {
            get { return Editor.M.ReadInt("0x0428DBA0") == 0; }
            set { Editor.M.WriteMemory("0x0428DBA0", "int", value ? "0" : "1"); }
        }
        private bool ActiveMetalAnimation
        {
            get { return Editor.M.ReadInt("0x0428DBB0") == 0; }
            set { Editor.M.WriteMemory("0x0428DBB0", "int", value ? "0" : "1"); }
        }
        private bool ActiveBoxes
        {
            get { return Editor.M.ReadInt("0x0428DBB8") == 0; }
            set { Editor.M.WriteMemory("0x0428DBB8", "int", value ? "0" : "1"); }
        }
        private bool ActiveConveyors
        {
            get { return Editor.M.ReadInt("0x0428DBC8") == 0; }
            set { Editor.M.WriteMemory("0x0428DBC8", "int", value ? "0" : "1"); }
        }
        private bool ActivePlayerCollision
        {
            get { return Editor.M.ReadInt("0x045A619C") == 0; }
            set { Editor.M.WriteMemory("0x045A619C", "int", value ? "0" : "1"); }
        }
        private bool ActiveRideArmor
        {
            //get { return Editor.M.ReadInt("0x0485A6CC") == 0; }
            set { Editor.M.WriteMemory("0x04857CC4", "int", value ? "0" : "1"); }
        }
        public bool ActivePlayer1
        {
            get { return Editor.M.ReadInt("0x045A6194") == 0; }
            set { Editor.M.WriteMemory("0x045A6194", "int", value ? "0" : "1"); }
        }
        public GameLevel CurrentLevelID
        {
            get { return (GameLevel)Editor.M.ReadInt("0x48CB7DC"); }
        }

        public SetFile CurrentLevelSetFile
        {
            get
            {
                if (_currentSet?.LevelID == CurrentLevelID)
                    return _currentSet;
                else
                {
                    _currentSet = new SetFile(CurrentLevelID);
                    return _currentSet;
                }
            }
        }
        private SetFile _currentSet;

        private void EnableGravity()
        {
            Editor.M.WriteMemory("0x04A1A80", "bytes", "0xD9 0x9E 0xD4 0x60 0x5A 0x04");
        }
        private void DisableGravity()
        {
            Editor.M.WriteMemory("0x04A1A80", "bytes", "0x90 0x90 0x90 0x90 0x90 0x90");
        }

        public void EnableEditMode()
        {
            ActiveEnemies = false;
            ActiveWind = false;
            ActiveMetalAnimation = false;
            ActiveBoxes = false;
            ActiveConveyors = false;
            ActivePlayerCollision = false;
            ActiveRideArmor = false;

            DisableGravity();
         }

        public void DisableEditMode()
        {
            ActiveEnemies = true;
            ActiveWind = true;
            ActiveMetalAnimation = true;
            ActiveBoxes = true;
            ActiveConveyors = true;
            ActivePlayerCollision = true;
            ActiveRideArmor = true;

            EnableGravity();
        }

        public Vec3 GetObjectVec(int objectID)
        {
            const int pStructSize = 0x47C;
            const int pCoordsBase = 0x045C284C;

            int offset = objectID * pStructSize;
            UIntPtr objectPtr = UIntPtr.Add((UIntPtr)pCoordsBase, offset);
            return new Vec3(objectPtr);
        }

        public void DisableOutOfFocus()
        {
            M.WriteMemory("NOCD.exe+3E8148C", "int", "65536");
        }
    }
}
