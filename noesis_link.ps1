# Directory where Noesis.EXE is
$noesisPath = "E:\Tools\noesis" 
$noesisPluginsPath = $noesisPath + "\plugins\python\"

# Directory where the X8 format plugins are in this repo
$x8PluginPath = ".\src\megaman-x8-tools\noesis\"
$wpgPluginFilename = "fmt_mmx8_wpg.py"
$wsxPluginFilename = "fmt_mmx8_wsx.py"

# Create symbolic links so Noesis can see and use the plugins
New-Item -ItemType SymbolicLink -Path "$noesisPluginsPath\$wpgPluginFilename" -Target "$x8PluginPath\$wpgPluginFilename"
New-Item -ItemType SymbolicLink -Path "$noesisPluginsPath\$wsxPluginFilename" -Target "$x8PluginPath\$wsxPluginFilename"

# Create a symbolic link so we can use Noesis' Python documentation and types
$noesisIncFilename = "inc_noesis.py"
$noesisIncPythonPath = $noesisPluginsPath + $noesisIncFilename
New-Item -ItemType SymbolicLink -Path "$x8PluginPath\$noesisIncFilename" -Target "$noesisIncPythonPath"