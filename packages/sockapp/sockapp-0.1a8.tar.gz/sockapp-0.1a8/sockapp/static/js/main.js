$(document).ready(function() {

    $("#send-file-nav").addClass("selected-nav-button");
    $("#send-message-nav").removeClass("selected-nav-button");
    
    $("#send").click(function() {
        var recv_ip = $("#recv_ip").val();
        var send_path = $("#send_path").val();

        Swal.fire({
            icon: "info",
            title: "Please wait...",
            text: "Sending file to receiver!"
        });

        if(recv_ip && send_path) {
            $.ajax({
                url: "/send",
                type: "post",
                dataType: "json",
                data: {"recv_ip": recv_ip, "send_path": send_path},
                success: function(result) {
                    window.swal.close();
                    Swal.fire({
                        icon: result.icon,
                        title: result.title,
                        text: result.status,
                    });
                }
            });
        } else {
            Swal.fire({
                icon: "error",
                title: "Error",
                text: "Both receiver IP and file path are required!",
            });
        }
    });

    $("#receive").click(function() {
        $("#receive").addClass("selected-button");

        Swal.fire({
            icon: "info",
            title: "Please wait...",
            text: "Receiving file from sender!"
        });

        $.ajax({
            url: "/receive",
            type: "post",
            dataType: "json",
            success: function(result) {
                window.swal.close();
                Swal.fire({
                    icon: result.icon,
                    title: result.title,
                    text: result.status,
                });
                $("#receive").removeClass("selected-button");
            }
        });
    });

});