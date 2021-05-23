/*
 * Some helpful notes taken from https://www.codeproject.com/Articles/9123/Hosting-EXE-Applications-in-a-WinForm-Project
 */
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;
using System.Runtime.InteropServices;
using Memory;

namespace src_GUI
{
    public partial class MainForm : Form
    {
        [DllImport("user32.dll")]
        static extern IntPtr SetParent(IntPtr hWndChild, IntPtr hWndNewParent);

        [DllImport("user32.dll")]
        static extern int SetWindowLong(IntPtr hWnd, int nIndex, int dwNewLong);

        [DllImport("user32.dll")]
        static extern bool MoveWindow(IntPtr Handle, int x, int y, int w, int h, bool repaint);

        static readonly int GWL_STYLE = -16;
        static readonly int WS_VISIBLE = 0x10000000;

        private Process GameProcess;
        private IntPtr GameHandle { get { if (GameProcess != null) return GameProcess.MainWindowHandle; return IntPtr.Zero; } }

        private Editor editor;

        private bool IsProcessOpen;
        public MainForm()
        {
            InitializeComponent();
        }

        private void MainForm_Shown(object sender, EventArgs e)
        {
            BGWorker.RunWorkerAsync();
            GamePanel.Size = new Size(1024, 768);

        }
        private void BGWorker_DoWork(object sender, DoWorkEventArgs e)
        {
            IsProcessOpen = Editor.M.OpenProcess("NOCD");
            Thread.Sleep(100);
            BGWorker.ReportProgress(0);
        }

        private void BGWorker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            BGWorker.RunWorkerAsync();
        }

        private void BGWorker_ProgressChanged(object sender, ProgressChangedEventArgs e)
        {
            if (IsProcessOpen)
            {
                //LblDebug.Text = "Game Loaded";
                LblDebug.ForeColor = Color.Green;

                BtnDebug.Enabled = false;
                TextP1X.Enabled = true;

                editor = new Editor();
                editor.DisableOutOfFocus();
            }
            else
            {
                LblDebug.Text = "Game Not Loaded";
                LblDebug.ForeColor = Color.Red;

                BtnDebug.Enabled = true;
                TextP1X.Enabled = false;
            }
        }

        private void BtnDebug_Click(object sender, EventArgs e)
        {
            try
            {
                ProcessStartInfo info = new ProcessStartInfo(@"C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\game\NOCD.exe");
                info.WorkingDirectory = @"C:\Users\xeroj\Desktop\Local_Programming\Python-RockManX8\game";
                info.UseShellExecute = false;
                info.CreateNoWindow = false;
                info.WindowStyle = ProcessWindowStyle.Normal;
                GameProcess = Process.Start(info);
                GameProcess.WaitForInputIdle();
                if (GameProcess.HasExited)
                {
                    LblDebug.Text = "Process has exited: " + GameProcess.ExitCode;
                }
                else
                {
                    SetParent(GameHandle, GamePanel.Handle);
                    SetWindowLong(GameProcess.MainWindowHandle, GWL_STYLE, WS_VISIBLE);
                    MoveWindow(GameProcess.MainWindowHandle, 0, 0, GamePanel.Width, GamePanel.Height, true);
                }
            }
            finally
            {
                GameProcess?.Close();
            }
        }

        private void MainForm_Resize(object sender, EventArgs e)
        {
        }

        private void MainForm_FormClosing(object sender, FormClosingEventArgs e)
        {
        }

        private void MainForm_FormClosed(object sender, FormClosedEventArgs e)
        {
            GameProcess?.Close();
        }

        private void MainForm_Load(object sender, EventArgs e)
        {

        }


        private void NumericObjectID_ValueChanged(object sender, EventArgs e)
        {
            //UIntPtr objectDataPtr = UIntPtr.Add(Mem.GetCode("NOCD.exe+0x045C284C"), (int)NumericObjectID.Value * 0x47C);
            int objectID = (int)NumericObjectID.Value;
            //int offset = objectID * 0x47C;
            //UIntPtr PCoordsBase = (UIntPtr)0x045C284C;
            //UIntPtr ObjectBase = UIntPtr.Add(PCoordsBase, offset);
            //float x1 = Mem.ReadPFloat(ObjectBase, "");
            //float y1 = Mem.ReadPFloat(UIntPtr.Add(ObjectBase, 4), "");
            //float z1 = Mem.ReadPFloat(UIntPtr.Add(ObjectBase, 8), "");

            //Vec3 v1 = new Vec3(ObjectBase);
            Vec3 v1 = editor.GetObjectVec(objectID);
            TextP1X.Text = v1.ToString();

            LblDebug.Text = editor.Player1Vec.ToString();
            if (objectID > 1)
                editor.Player1Vec.Set(v1);
            //    MovePlayer1(x1, y1, z1);
        }

        private void NumericObjectX_ValueChanged(object sender, EventArgs e)
        {
            Console.WriteLine("X CHANGED");
        }

        private void MovePlayer1(float x, float y, float z)
        {
            //Mem.WriteMemory("NOCD.exe+0x41A61F8", "float", x.ToString());
        }

        private void NumericObjectY_ValueChanged(object sender, EventArgs e)
        {

        }

        private void NumericObjectZ_ValueChanged(object sender, EventArgs e)
        {

        }
    }
}
