<?php

$Name = $_POST['Name'] ?? '';
$Email = $_POST['Email'] ?? '';
$Password = $_POST['Password'] ?? '';
$Mobile = $_POST['Mobile'] ?? '';

if (!empty($Name) && !empty($Email) && !empty($Password) && !empty($Mobile)) {
    $host = "localhost";
    $dbusername = "root";
    $dbpassword = "";
    $dbname = "musio";

    $conn = new mysqli($host, $dbusername, $dbpassword, $dbname);

    if ($conn->connect_error) {
        die('Connect Error (' . $conn->connect_errno . ') ' . $conn->connect_error);
    } else {
        $SELECT = "SELECT Email FROM signup WHERE Email = ? LIMIT 1";
        $INSERT = "INSERT INTO signup (Name, Email, Password, Mobile) VALUES (?, ?, ?, ?)";

        $stmt = $conn->prepare($SELECT);
        $stmt->bind_param("s", $Email);
        $stmt->execute();
        $stmt->bind_result($Email);
        $stmt->store_result();
        $rnum = $stmt->num_rows;

        if ($rnum == 0) {
            $stmt->close();
            $stmt = $conn->prepare($INSERT);
            $stmt->bind_param("ssss", $Name, $Email, $Password, $Mobile);
            $stmt->execute();
            echo "New record inserted successfully";
        } else {
            echo "Someone already registered using this email";
        }
        $stmt->close();
        $conn->close();
    }
} else {
    echo "All fields are required";
    die();
}
