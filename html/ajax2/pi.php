<?php
$welcomefile=file('haha.txt'); //返回数组的内容
foreach($welcomefile as $v){
        echo $v.'<br>';
}?>