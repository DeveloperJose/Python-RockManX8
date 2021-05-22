
namespace src_GUI
{
    partial class MainForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.BGWorker = new System.ComponentModel.BackgroundWorker();
            this.LblDebug = new System.Windows.Forms.Label();
            this.BtnDebug = new System.Windows.Forms.Button();
            this.GamePanel = new System.Windows.Forms.Panel();
            this.label1 = new System.Windows.Forms.Label();
            this.TextP1X = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // BGWorker
            // 
            this.BGWorker.WorkerReportsProgress = true;
            this.BGWorker.DoWork += new System.ComponentModel.DoWorkEventHandler(this.BGWorker_DoWork);
            this.BGWorker.ProgressChanged += new System.ComponentModel.ProgressChangedEventHandler(this.BGWorker_ProgressChanged);
            this.BGWorker.RunWorkerCompleted += new System.ComponentModel.RunWorkerCompletedEventHandler(this.BGWorker_RunWorkerCompleted);
            // 
            // LblDebug
            // 
            this.LblDebug.AutoSize = true;
            this.LblDebug.Location = new System.Drawing.Point(25, 28);
            this.LblDebug.Name = "LblDebug";
            this.LblDebug.Size = new System.Drawing.Size(45, 13);
            this.LblDebug.TabIndex = 0;
            this.LblDebug.Text = "Debug: ";
            // 
            // BtnDebug
            // 
            this.BtnDebug.Location = new System.Drawing.Point(921, 18);
            this.BtnDebug.Name = "BtnDebug";
            this.BtnDebug.Size = new System.Drawing.Size(75, 23);
            this.BtnDebug.TabIndex = 2;
            this.BtnDebug.Text = "Load";
            this.BtnDebug.UseVisualStyleBackColor = true;
            this.BtnDebug.Click += new System.EventHandler(this.BtnDebug_Click);
            // 
            // GamePanel
            // 
            this.GamePanel.BackColor = System.Drawing.SystemColors.ActiveCaption;
            this.GamePanel.Location = new System.Drawing.Point(0, 0);
            this.GamePanel.Name = "GamePanel";
            this.GamePanel.Size = new System.Drawing.Size(20, 20);
            this.GamePanel.TabIndex = 3;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(183, 23);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(30, 13);
            this.label1.TabIndex = 4;
            this.label1.Text = "P1 X";
            // 
            // TextP1X
            // 
            this.TextP1X.Location = new System.Drawing.Point(219, 20);
            this.TextP1X.Name = "TextP1X";
            this.TextP1X.Size = new System.Drawing.Size(100, 20);
            this.TextP1X.TabIndex = 5;
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1035, 776);
            this.Controls.Add(this.TextP1X);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.BtnDebug);
            this.Controls.Add(this.LblDebug);
            this.Controls.Add(this.GamePanel);
            this.Name = "MainForm";
            this.Text = "Mega Man X8 Editor by Rainfall";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.MainForm_FormClosing);
            this.FormClosed += new System.Windows.Forms.FormClosedEventHandler(this.MainForm_FormClosed);
            this.Shown += new System.EventHandler(this.MainForm_Shown);
            this.Resize += new System.EventHandler(this.MainForm_Resize);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.ComponentModel.BackgroundWorker BGWorker;
        private System.Windows.Forms.Label LblDebug;
        private System.Windows.Forms.Button BtnDebug;
        private System.Windows.Forms.Panel GamePanel;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox TextP1X;
    }
}

