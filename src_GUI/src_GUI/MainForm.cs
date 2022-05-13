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
        private bool IsEditModeActive;
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
        }

        private void MainForm_Load(object sender, EventArgs e)
        {

        }


        private void NumericObjectID_ValueChanged(object sender, EventArgs e)
        {
            /*
            int objectID = (int)MemoryObjectID.Value;

            Vec3 v1 = editor.GetObjectVec(objectID);
            TextP1X.Text = v1.ToString();

            LblDebug.Text = editor.Player1Vec.ToString();
            if (objectID > 1)
            {
                editor.Player1Vec.Set(v1);
            }
            */
        }

        private void NumericObjectX_ValueChanged(object sender, EventArgs e)
        {
            Console.WriteLine("X CHANGED");
            int objectID = (int)MemoryObjectID.Value;
            Vec3 v1 = editor.GetObjectVec(objectID);
            v1.X = (float)MemoryX.Value;
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

        private void BtnToggleEditMode_Click(object sender, EventArgs e)
        {
            IsEditModeActive = !IsEditModeActive;

            if (IsEditModeActive)
            {
                editor.EnableEditMode();
                BtnToggleEditMode.Text = "Stop Edit";
            }
            else
            {
                editor.DisableEditMode();
                BtnToggleEditMode.Text = "Start Edit";
            }
        }

        private void SetFileObjectID_ValueChanged(object sender, EventArgs e)
        {
            int setObjectID = (int)SetFileObjectID.Value;
            SetEnemy currentEnemy = editor.CurrentLevelSetFile.Enemies[setObjectID];
            SetFileX.Value = (decimal)currentEnemy.X;
            SetFileY.Value = (decimal)currentEnemy.Y;
            SetFileZ.Value = (decimal)currentEnemy.Z;
            SetFilePrm.Text = currentEnemy.PrmStr;

            editor.Player1Vec.Set(currentEnemy.X, currentEnemy.Y, editor.Player1Vec.Z);

            // Disable controls for now
            MemoryObjectID.Enabled = false;
            MemoryX.Enabled = false;
            MemoryY.Enabled = false;
            MemoryZ.Enabled = false;

            // Look inside the memory for this object?
            Vec3 possibleVec = editor.GetObjectVec(2);
            int i = 2;
            while(possibleVec.IsValid || i < 15)
            {
                if (possibleVec.Equals(currentEnemy.X, currentEnemy.Y, currentEnemy.Z))
                {
                    MemoryObjectID.Enabled = true;
                    MemoryX.Enabled = true;
                    MemoryY.Enabled = true;
                    MemoryZ.Enabled = true;

                    MemoryObjectID.Value = i;
                    MemoryX.Value = (decimal)possibleVec.X;
                    MemoryY.Value = (decimal)possibleVec.Y;
                    MemoryZ.Value = (decimal)possibleVec.Z;
                    break;
                }
                i++;
                possibleVec = editor.GetObjectVec(i);
            };
        }
    }
}
