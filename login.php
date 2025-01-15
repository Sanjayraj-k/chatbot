<?php
$conn = new mysqli("localhost", "root", "", "musio");

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if (isset($_SERVER["REQUEST_METHOD"]) && $_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $conn->real_escape_string($_POST['Email']);
    $password = $conn->real_escape_string($_POST['Password']);
=
    $sql = "SELECT * FROM signup WHERE Email = '$email'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $user = $result->fetch_assoc();
        if ($password === $user['Password']) {
            session_start();
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['email'] = $user['Email'];
            header("Location: index.html");
            exit;
        } else {
            echo "Error: Incorrect password!";
        }
    } else {
        echo "Error: No account found with that email!";
    }
} else {
    echo "Invalid access. Please submit the form.";
}

$conn->close();
?>
