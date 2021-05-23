
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
            this.label2 = new System.Windows.Forms.Label();
            this.NumericObjectID = new System.Windows.Forms.NumericUpDown();
            this.label3 = new System.Windows.Forms.Label();
            this.NumericObjectX = new System.Windows.Forms.NumericUpDown();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.NumericObjectY = new System.Windows.Forms.NumericUpDown();
            this.NumericObjectZ = new System.Windows.Forms.NumericUpDown();
            ((System.ComponentModel.ISupportInitialize)(this.NumericObjectID)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.NumericObjectX)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.NumericObjectY)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.NumericObjectZ)).BeginInit();
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
            this.LblDebug.Location = new System.Drawing.Point(941, 9);
            this.LblDebug.Name = "LblDebug";
            this.LblDebug.Size = new System.Drawing.Size(45, 13);
            this.LblDebug.TabIndex = 0;
            this.LblDebug.Text = "Debug: ";
            // 
            // BtnDebug
            // 
            this.BtnDebug.Location = new System.Drawing.Point(925, 25);
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
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(622, 9);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(14, 13);
            this.label2.TabIndex = 6;
            this.label2.Text = "X";
            // 
            // NumericObjectID
            // 
            this.NumericObjectID.Location = new System.Drawing.Point(549, 7);
            this.NumericObjectID.Name = "NumericObjectID";
            this.NumericObjectID.Size = new System.Drawing.Size(55, 20);
            this.NumericObjectID.TabIndex = 8;
            this.NumericObjectID.ValueChanged += new System.EventHandler(this.NumericObjectID_ValueChanged);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(454, 9);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(89, 13);
            this.label3.TabIndex = 9;
            this.label3.Text = "Current Object ID";
            // 
            // NumericObjectX
            // 
            this.NumericObjectX.Location = new System.Drawing.Point(642, 7);
            this.NumericObjectX.Name = "NumericObjectX";
            this.NumericObjectX.Size = new System.Drawing.Size(71, 20);
            this.NumericObjectX.TabIndex = 10;
            this.NumericObjectX.ValueChanged += new System.EventHandler(this.NumericObjectX_ValueChanged);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(600, 34);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(14, 13);
            this.label4.TabIndex = 11;
            this.label4.Text = "Y";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(605, 63);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(14, 13);
            this.label5.TabIndex = 12;
            this.label5.Text = "Z";
            // 
            // NumericObjectY
            // 
            this.NumericObjectY.Location = new System.Drawing.Point(625, 34);
            this.NumericObjectY.Name = "NumericObjectY";
            this.NumericObjectY.Size = new System.Drawing.Size(120, 20);
            this.NumericObjectY.TabIndex = 13;
            this.NumericObjectY.ValueChanged += new System.EventHandler(this.NumericObjectY_ValueChanged);
            // 
            // NumericObjectZ
            // 
            this.NumericObjectZ.Location = new System.Drawing.Point(625, 61);
            this.NumericObjectZ.Name = "NumericObjectZ";
            this.NumericObjectZ.Size = new System.Drawing.Size(120, 20);
            this.NumericObjectZ.TabIndex = 14;
            this.NumericObjectZ.ValueChanged += new System.EventHandler(this.NumericObjectZ_ValueChanged);
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1035, 776);
            this.Controls.Add(this.NumericObjectZ);
            this.Controls.Add(this.NumericObjectY);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.NumericObjectX);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.NumericObjectID);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.TextP1X);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.BtnDebug);
            this.Controls.Add(this.LblDebug);
            this.Controls.Add(this.GamePanel);
            this.Name = "MainForm";
            this.Text = "Mega Man X8 Editor by Rainfall";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.MainForm_FormClosing);
            this.FormClosed += new System.Windows.Forms.FormClosedEventHandler(this.MainForm_FormClosed);
            this.Load += new System.EventHandler(this.MainForm_Load);
            this.Shown += new System.EventHandler(this.MainForm_Shown);
            this.Resize += new System.EventHandler(this.MainForm_Resize);
            ((System.ComponentModel.ISupportInitialize)(this.NumericObjectID)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.NumericObjectX)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.NumericObjectY)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.NumericObjectZ)).EndInit();
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
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.NumericUpDown NumericObjectID;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.NumericUpDown NumericObjectX;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.NumericUpDown NumericObjectY;
        private System.Windows.Forms.NumericUpDown NumericObjectZ;
    }
}

