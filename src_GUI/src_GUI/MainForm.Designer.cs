
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
            this.MemoryObjectID = new System.Windows.Forms.NumericUpDown();
            this.label3 = new System.Windows.Forms.Label();
            this.MemoryX = new System.Windows.Forms.NumericUpDown();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.MemoryY = new System.Windows.Forms.NumericUpDown();
            this.MemoryZ = new System.Windows.Forms.NumericUpDown();
            this.BtnToggleEditMode = new System.Windows.Forms.Button();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.SetFilePrm = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.SetFileObjectID = new System.Windows.Forms.NumericUpDown();
            this.label7 = new System.Windows.Forms.Label();
            this.SetFileZ = new System.Windows.Forms.NumericUpDown();
            this.SetFileX = new System.Windows.Forms.NumericUpDown();
            this.label8 = new System.Windows.Forms.Label();
            this.SetFileY = new System.Windows.Forms.NumericUpDown();
            this.label9 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.MemoryObjectID)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.MemoryX)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.MemoryY)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.MemoryZ)).BeginInit();
            this.groupBox1.SuspendLayout();
            this.groupBox2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.SetFileObjectID)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.SetFileZ)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.SetFileX)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.SetFileY)).BeginInit();
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
            this.label2.Location = new System.Drawing.Point(118, 16);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(14, 13);
            this.label2.TabIndex = 6;
            this.label2.Text = "X";
            // 
            // MemoryObjectID
            // 
            this.MemoryObjectID.Location = new System.Drawing.Point(33, 32);
            this.MemoryObjectID.Name = "MemoryObjectID";
            this.MemoryObjectID.Size = new System.Drawing.Size(40, 20);
            this.MemoryObjectID.TabIndex = 8;
            this.MemoryObjectID.ValueChanged += new System.EventHandler(this.NumericObjectID_ValueChanged);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(6, 16);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(92, 13);
            this.label3.TabIndex = 9;
            this.label3.Text = "Current Object ID:";
            // 
            // MemoryX
            // 
            this.MemoryX.Location = new System.Drawing.Point(105, 32);
            this.MemoryX.Maximum = new decimal(new int[] {
            1000,
            0,
            0,
            0});
            this.MemoryX.Minimum = new decimal(new int[] {
            1000,
            0,
            0,
            -2147483648});
            this.MemoryX.Name = "MemoryX";
            this.MemoryX.Size = new System.Drawing.Size(40, 20);
            this.MemoryX.TabIndex = 10;
            this.MemoryX.ValueChanged += new System.EventHandler(this.NumericObjectX_ValueChanged);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(177, 16);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(14, 13);
            this.label4.TabIndex = 11;
            this.label4.Text = "Y";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(234, 16);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(14, 13);
            this.label5.TabIndex = 12;
            this.label5.Text = "Z";
            // 
            // MemoryY
            // 
            this.MemoryY.Location = new System.Drawing.Point(165, 32);
            this.MemoryY.Maximum = new decimal(new int[] {
            1000,
            0,
            0,
            0});
            this.MemoryY.Minimum = new decimal(new int[] {
            1000,
            0,
            0,
            -2147483648});
            this.MemoryY.Name = "MemoryY";
            this.MemoryY.Size = new System.Drawing.Size(40, 20);
            this.MemoryY.TabIndex = 13;
            this.MemoryY.ValueChanged += new System.EventHandler(this.NumericObjectY_ValueChanged);
            // 
            // MemoryZ
            // 
            this.MemoryZ.Location = new System.Drawing.Point(222, 32);
            this.MemoryZ.Maximum = new decimal(new int[] {
            1000,
            0,
            0,
            0});
            this.MemoryZ.Minimum = new decimal(new int[] {
            1000,
            0,
            0,
            -2147483648});
            this.MemoryZ.Name = "MemoryZ";
            this.MemoryZ.Size = new System.Drawing.Size(40, 20);
            this.MemoryZ.TabIndex = 14;
            this.MemoryZ.ValueChanged += new System.EventHandler(this.NumericObjectZ_ValueChanged);
            // 
            // BtnToggleEditMode
            // 
            this.BtnToggleEditMode.Location = new System.Drawing.Point(13, 52);
            this.BtnToggleEditMode.Name = "BtnToggleEditMode";
            this.BtnToggleEditMode.Size = new System.Drawing.Size(75, 23);
            this.BtnToggleEditMode.TabIndex = 15;
            this.BtnToggleEditMode.Text = "Start Edit";
            this.BtnToggleEditMode.UseVisualStyleBackColor = true;
            this.BtnToggleEditMode.Click += new System.EventHandler(this.BtnToggleEditMode_Click);
            // 
            // groupBox1
            // 
            this.groupBox1.BackColor = System.Drawing.SystemColors.ActiveCaption;
            this.groupBox1.Controls.Add(this.label3);
            this.groupBox1.Controls.Add(this.MemoryObjectID);
            this.groupBox1.Controls.Add(this.label2);
            this.groupBox1.Controls.Add(this.MemoryZ);
            this.groupBox1.Controls.Add(this.MemoryX);
            this.groupBox1.Controls.Add(this.label5);
            this.groupBox1.Controls.Add(this.MemoryY);
            this.groupBox1.Controls.Add(this.label4);
            this.groupBox1.Location = new System.Drawing.Point(437, 25);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(274, 64);
            this.groupBox1.TabIndex = 16;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "In-Game Memory (Temporary)";
            // 
            // groupBox2
            // 
            this.groupBox2.BackColor = System.Drawing.SystemColors.ActiveCaption;
            this.groupBox2.Controls.Add(this.label6);
            this.groupBox2.Controls.Add(this.SetFilePrm);
            this.groupBox2.Controls.Add(this.SetFileObjectID);
            this.groupBox2.Controls.Add(this.SetFileX);
            this.groupBox2.Controls.Add(this.label7);
            this.groupBox2.Controls.Add(this.label9);
            this.groupBox2.Controls.Add(this.SetFileZ);
            this.groupBox2.Controls.Add(this.SetFileY);
            this.groupBox2.Controls.Add(this.label8);
            this.groupBox2.Location = new System.Drawing.Point(437, 95);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(274, 100);
            this.groupBox2.TabIndex = 17;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Set File (Permanent)";
            // 
            // SetFilePrm
            // 
            this.SetFilePrm.Location = new System.Drawing.Point(168, 54);
            this.SetFilePrm.Name = "SetFilePrm";
            this.SetFilePrm.Size = new System.Drawing.Size(100, 20);
            this.SetFilePrm.TabIndex = 0;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(6, 15);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(92, 13);
            this.label6.TabIndex = 17;
            this.label6.Text = "Current Object ID:";
            // 
            // SetFileObjectID
            // 
            this.SetFileObjectID.Location = new System.Drawing.Point(33, 31);
            this.SetFileObjectID.Name = "SetFileObjectID";
            this.SetFileObjectID.Size = new System.Drawing.Size(40, 20);
            this.SetFileObjectID.TabIndex = 16;
            this.SetFileObjectID.ValueChanged += new System.EventHandler(this.SetFileObjectID_ValueChanged);
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(118, 15);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(14, 13);
            this.label7.TabIndex = 15;
            this.label7.Text = "X";
            // 
            // SetFileZ
            // 
            this.SetFileZ.Location = new System.Drawing.Point(222, 31);
            this.SetFileZ.Maximum = new decimal(new int[] {
            1000,
            0,
            0,
            0});
            this.SetFileZ.Minimum = new decimal(new int[] {
            1000,
            0,
            0,
            -2147483648});
            this.SetFileZ.Name = "SetFileZ";
            this.SetFileZ.Size = new System.Drawing.Size(40, 20);
            this.SetFileZ.TabIndex = 22;
            // 
            // SetFileX
            // 
            this.SetFileX.Location = new System.Drawing.Point(105, 31);
            this.SetFileX.Maximum = new decimal(new int[] {
            1000,
            0,
            0,
            0});
            this.SetFileX.Minimum = new decimal(new int[] {
            1000,
            0,
            0,
            -2147483648});
            this.SetFileX.Name = "SetFileX";
            this.SetFileX.Size = new System.Drawing.Size(40, 20);
            this.SetFileX.TabIndex = 18;
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(234, 15);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(14, 13);
            this.label8.TabIndex = 20;
            this.label8.Text = "Z";
            // 
            // SetFileY
            // 
            this.SetFileY.Location = new System.Drawing.Point(165, 31);
            this.SetFileY.Maximum = new decimal(new int[] {
            1000,
            0,
            0,
            0});
            this.SetFileY.Minimum = new decimal(new int[] {
            1000,
            0,
            0,
            -2147483648});
            this.SetFileY.Name = "SetFileY";
            this.SetFileY.Size = new System.Drawing.Size(40, 20);
            this.SetFileY.TabIndex = 21;
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(177, 15);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(14, 13);
            this.label9.TabIndex = 19;
            this.label9.Text = "Y";
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1035, 776);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.BtnToggleEditMode);
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
            ((System.ComponentModel.ISupportInitialize)(this.MemoryObjectID)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.MemoryX)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.MemoryY)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.MemoryZ)).EndInit();
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.SetFileObjectID)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.SetFileZ)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.SetFileX)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.SetFileY)).EndInit();
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
        private System.Windows.Forms.NumericUpDown MemoryObjectID;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.NumericUpDown MemoryX;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.NumericUpDown MemoryY;
        private System.Windows.Forms.NumericUpDown MemoryZ;
        private System.Windows.Forms.Button BtnToggleEditMode;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.TextBox SetFilePrm;
        private System.Windows.Forms.NumericUpDown SetFileObjectID;
        private System.Windows.Forms.NumericUpDown SetFileX;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.NumericUpDown SetFileZ;
        private System.Windows.Forms.NumericUpDown SetFileY;
        private System.Windows.Forms.Label label8;
    }
}

