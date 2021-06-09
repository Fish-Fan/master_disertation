define([], function () {
    // jsPlumb.ready(function() {
        //socket connection start
        // var socket = io();
        // socket.on('connect', function() {
        //     socket.emit('handle_my_event', {data: 'I\'m connected!'}, (response) => {
        //         console.log(response)
        //     });
        // });
        // socket.on('myemit', (response) => {
        //     var modal_id = "myemit";
        //     var container_id = "myemit_container";
        //     var showSourceModal = Util.getModal(modal_id, "Receive message from server", function(modal) {
        //         var body = modal.select(".modal-body");
        //         body.attr("id", container_id).style("overflow", "auto");
        //     });
        //
        //     $("#" + container_id).empty();
        //     d3.select("#" + container_id).append("pre").attr("id", "myemit_text").append('p').text(response);
        //     $("#" + modal_id).modal("show");
        // });
    // });
    var Socket = io();
    Socket.post_files = (data) => {
        Socket.emit('post_files', data, (response) => {
            console.log(response)
        })
    };
    Socket.post_datetime_column = (data) => {
        Socket.emit('post_datetime_column', data, (response) => {
            console.log(response)
        })
    };
    return Socket;
});