# Push-Location .\kaitai_struct_compiler\
# sbt --error compilerJVM/stage
# Pop-Location

$kaitaiPath = ".\_arc\kaitai_struct_compiler\jvm\target\universal\stage\bin\kaitai-struct-compiler"
$argList = "--read-write --no-auto-read -d .\kaitai -t python .\kaitai\set.ksy"
Start-Process -FilePath $kaitaiPath -ArgumentList $argList -Wait -NoNewWindow
