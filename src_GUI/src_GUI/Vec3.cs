using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Memory;
namespace src_GUI
{
    public class Vec3
    {
        public float X
        {
            get
            {
                return Editor.M.ReadPFloat(Ptr, "0");
            }
            set
            {
                Editor.M.WriteMemory(string.Format("{0:X}", (int)Ptr), "float", value.ToString());
            }
        }
        public float Y
        {
            get
            {
                return Editor.M.ReadPFloat(UIntPtr.Add(Ptr, 4), "0");
            }
            set
            {
                Editor.M.WriteMemory(string.Format("{0:X}", (int)UIntPtr.Add(Ptr, 4)), "float", value.ToString());
            }
        }
        public float Z
        {
            get
            {
                return Editor.M.ReadPFloat(UIntPtr.Add(Ptr, 8), "0");
            }
            set
            {
                Editor.M.WriteMemory(string.Format("{0:X}", (int)UIntPtr.Add(Ptr, 8)), "float", value.ToString());
            }
        }

        private readonly UIntPtr Ptr;
        public Vec3(UIntPtr ptr)
        {
            Ptr = ptr;
        }

        public void Set(Vec3 other)
        {
            Set(other.X, other.Y, other.Z);
        }

        public void Set(float x, float y, float z)
        {
            X = x;
            Y = y;
            Z = z;
        }

        public override string ToString()
        {
            return string.Format("Vec3(p={0}|x={1},y={2},z={3}", Ptr, X, Y, Z);
        }
    }
}
