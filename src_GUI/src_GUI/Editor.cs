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
            //M.FreezeValue("NOCD.exe+3E8148C", "int", "65536");
            M.WriteMemory("NOCD.exe+3E8148C", "int", "65536");
        }
    }
}
