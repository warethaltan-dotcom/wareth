using System;
using System.Windows.Forms;
using Listener.Config;
using Listener.Logger;

namespace Listener
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            LogManager.Init();
            var cfg = ConfigManager.Load();
            Application.Run(new UI.MainForm());
        }
    }
}
