define([], function() {
	var Util = {};
	
    Util.addPanel = function(parent, title) {
        var panel = parent.append("div").classed("panel panel-default", true);
        if (title != undefined) {
            panel.append("div").classed("panel-heading", true).text(title);
        }
        panel.append("div").classed("panel-body", true);

        return panel
    };

    Util.getModal = function(id, title, init) { 
        if ( Util[id] !== undefined ) {
            return Util[id];
        }

        var modal = d3.select("body").append("div");
        Util[id] = modal;
        modal.attr("id",id);

        modal.classed("modal fade",true).attr("tableindex","-1").attr("role","dialog");
        var dialog = modal.append("div").classed("modal-dialog",true).attr("role","document");
        var content = dialog.append("div").classed("modal-content",true);
        var header = content.append("div").classed("modal-header",true);
        header.append("button").classed("close",true).attr("data-dismiss","modal").attr("aria-label","Close").append("span").attr("aria-hidden",true).text("x");
        header.append("h4").classed("modal-title",true).text(title);
        var body = content.append("div").classed("modal-body",true);
        var footer = content.append("div").classed("modal-footer",true);
        footer.append("button").attr("type","button").classed("btn btn-default",true).attr("data-dismiss","modal").text("Close");

        // call init function to initialize the modal dialog
        init.call(Util, modal);

        return modal;
    };

    Util.generateModalwithInput = function(id, title, dataset,type,confirmCallback) {
        var modal_id = id + "_modal";
        var container_id = id + "_container";
        var inputname = id + '_' + type;
        $("#" + container_id).empty();

        Util.getModal(modal_id, title, function (modal) {
            var body = modal.select(".modal-body");
            body.attr("id", container_id).style("overflow", "auto");
            var footer = modal.select(".modal-footer");
            footer.append("button").attr("type", "button").classed("btn btn-default", true).attr("data-dismiss", "modal").text("Confirm").on("click", confirmCallback)
        });

        d3.select("#" + container_id).append("ul").selectAll("li").data(dataset).enter().append("li").append("div").attr('class','checkbox checkbox-primary').html(function(d) {
            return "<input name="+ inputname + " type="+ type +" value='"+ d +"'/><label for='"+ inputname +"'>"+ d +"</label>"
        });

        $("#" + modal_id).modal("show");
    };

    return Util;
});
