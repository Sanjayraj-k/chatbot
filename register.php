<?php
$conn = new mysqli("localhost", "root", "", "musio");

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
if (isset($_SERVER["REQUEST_METHOD"]) && $_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $conn->real_escape_string($_POST['Name']);
    $email = $conn->real_escape_string($_POST['Email']);
    $password = $conn->real_escape_string($_POST['Password']);
    $mobile = $conn->real_escape_string($_POST['Mobile']);

    $checkEmailQuery = "SELECT * FROM signup WHERE Email = '$email'";
    $result = $conn->query($checkEmailQuery);

    if ($result->num_rows > 0) {
        echo "Error: Email already exists!";
    } else {
        $sql = "INSERT INTO signup (Name, Email, Password, Mobile) VALUES ('$name', '$email', '$password', '$mobile')";

        if ($conn->query($sql) === TRUE) {
            header("Location: login.html");
            exit;
        } else {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
    }
} else {
    echo "Invalid access. Please submit the form.";
}

$conn->close();
?>
