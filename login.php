<?php
$conn=mysqli_connect("localhost","root","","loginbot");
if($conn){
    echo "Connected ";
}
else{
    echo "Failed";
}
?>