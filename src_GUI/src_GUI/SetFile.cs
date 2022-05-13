using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace src_GUI
{
    public class SetEnemy
    {
        public byte[] U1 { get; set; }
        public int ID { get; set; }
        public byte[] U2  { get; set; }
        public float X { get; set; }
        public float Y { get; set; }
        public float Z { get; set; }
        public byte[] U3 { get; set; }
        public int K1 { get; set; }
        public byte[] U4 { get; set; }
        public string PrmStr { get; set; }
        public byte[] U5 { get; set; }

        public SetEnemy(BinaryReader reader)
        {
            U1 = reader.ReadBytes(6);
            ID = reader.ReadInt16();
            U2 = reader.ReadBytes(8);
            X = reader.ReadSingle();
            Y = reader.ReadSingle();
            Z = reader.ReadSingle();
            U3 = reader.ReadBytes(4);
            K1 = reader.ReadInt16();
            U4 = reader.ReadBytes(6);
            PrmStr = new string(reader.ReadChars(8));
            U5 = reader.ReadBytes(32);
        }
    }
    public class SetFile
    {
        public List<SetEnemy> Enemies { get; private set; }
        public GameLevel LevelID { get; private set; }

        public SetFile(GameLevel gameLevelID)
        {
            this.Enemies = new List<SetEnemy>();
            this.LevelID = gameLevelID;

            string path = string.Format(@"C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\game\set\Set{0:D2}_00.set", (int)gameLevelID);
            using (BinaryReader reader = new BinaryReader(File.OpenRead(path)))
            {
                int numEnemies = reader.ReadInt16();
                byte[] header = reader.ReadBytes(0x3E);

                for (int i = 0; i < numEnemies; i++)
                {
                    Enemies.Add(new SetEnemy(reader));
                }
            }
        }
    }
}
