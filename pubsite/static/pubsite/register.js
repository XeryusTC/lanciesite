$(document).ready(function() {
    $("input:checkbox").change(function() {
        friday = bool_to_int($("#id_friday").prop("checked"));
        saturday = bool_to_int($("#id_saturday").prop("checked"));
        sunday = bool_to_int($("#id_sunday").prop("checked"));
        transport = bool_to_int($("#id_transport").prop("checked"));
        member = bool_to_int($("#id_cover_member").prop("checked"));
        url = "/price/" + friday + "/" + saturday + "/" + sunday + "/" + transport + "/" + member + "/";
        $.getJSON(url, function(data) {
            $("#price").html("&euro; " + data['price'] + ",-");
        });
    });
});

function bool_to_int(value) {
    if (value) {
        return "1"
    } else {
        return "0"
    }
}
