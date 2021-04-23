<?php
if ($_POST["pwd"] == "thepassword")
{
    echo "You entered the protected page successfully";
    header( 'Location: ngc6791.html' );
}
?>