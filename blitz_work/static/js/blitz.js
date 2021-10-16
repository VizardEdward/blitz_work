function cancelSelection() {
    $(".blitzCheck").each(function () {
        $(this).prop("checked", false);
        $(this).parent().parent().parent().removeClass("table-secondary");
    });
    $(".blitzSelectionButtons").toggle(false);
    $(".blitzCheckAll").prop("checked", false);
}
function getSelected(url) {
    let selection = [];
    $(".blitzCheck").each(function () {
        if ($(this).prop("checked") == true) {
            $(this)
                .parent()
                .parent()
                .siblings("input")
                .each(function () {
                    selection.push($(this).val());
                });
        }
    });
    window.location = url + "?item=" + selection.join("&item=");
}
$(document).ready(function () {
    function checkSelected() {
        let all = true;
        let selection = false;
        $(".blitzCheck").each(function () {
            if ($(this).prop("checked")) {
                selection = true;
            } else {
                all = false;
            }
        });
        $(".blitzSelectionButtons").toggle(selection);
        $(".blitzCheckAll").prop("checked", all);
    }
    function getStorageFixedUrl(url) {
        let pos = url.indexOf("?", url.lastIndexOf("/"));
        if (pos > 0) {
            pos = url.indexOf("search=", pos);
            if (pos > 0) {
                return url.substring(0, pos);
            } else {
                return url + "&";
            }
        } else {
            return url + "?";
        }
    }
    function getFixedUrl(url) {
        let pos = url.indexOf("?", url.lastIndexOf("/"));
        if (pos > 0) {
            pos = url.indexOf("search=", pos);
            if (pos > 0) {
                return url.substring(0, pos - 1);
            } else {
                return url;
            }
        } else {
            return url;
        }
    }
    $("table").on("change", ".blitzCheckAll", function () {
        let value = $(this).prop("checked");
        $(this)
            .closest("table")
            .find("tbody")
            .children()
            .each(function () {
                $(this).find("th div input").prop("checked", value);
                if (value) {
                    $(this).addClass("table-secondary");
                } else {
                    $(this).removeClass("table-secondary");
                }
            });
        checkSelected();
    });
    $("table").on("change", ".blitzCheck", function () {
        $(this).closest("tr").toggleClass("table-secondary");
        if (!$(this).prop("checked")) {
            $(this)
                .closest("table")
                .find("input.blitzCheckAll")
                .prop("checked", false);
        }
        checkSelected();
    });
    $("#blitzCrudSearchButton").click(function () {
        let textSearch = $("#blitzCrudSearchInput").val();
        let storageUrl =
            getStorageFixedUrl(window.location.href) + "search=" + textSearch;
        let url = getFixedUrl(window.location.href);
        window.history.pushState({ href: storageUrl }, "", storageUrl);
        $.ajax({
            method: "GET",
            url: url,
            data: { search: textSearch },
            success: function (response) {
                $("table").html($("table", response).html());
                $("ul.pagination").html($("ul.pagination", response).html());
                checkSelected();
            },
        });
    });
    checkSelected();
    $(".blitzSelect").select2({
        theme: "bootstrap4",
        width: "form-control",
    });
    $("#blitzCrudSearchInput").keyup(function (event) {
        if (event.keyCode === 13) {
            $("#blitzCrudSearchButton").click();
            event.preventDefault();
        }
    });
    $("fieldset[disabled] select").prop("disabled", true);
    $("#blitz-dark-mode-switch").change(function () {
        let value = $(this).prop("checked");
        if (value) {
            $(document.body)
                .removeClass("bootstrap")
                .addClass("bootstrap-dark");
            localStorage.setItem("blitz-dark-mode", true);
            console.log(localStorage.getItem("blitz-dark-mode"));
        } else {
            $(document.body)
                .removeClass("bootstrap-dark")
                .addClass("bootstrap");
            localStorage.setItem("blitz-dark-mode", false);
        }
    });
    if (localStorage.getItem("blitz-dark-mode") === "true") {
        $("#blitz-dark-mode-switch").prop("checked", true);
        $(document.body).removeClass("bootstrap").addClass("bootstrap-dark");
    } else {
        $("#blitz-dark-mode-switch").prop("checked", false);
        $(document.body).removeClass("bootstrap-dark").addClass("bootstrap");
        localStorage.setItem("blitz-dark-mode", false);
    }
    $(".date-time-picker").each(function(){
        time = moment($(this).val());
        $(this).datetimepicker({
            date: time,
        icons: {
            time: "fas fa-clock",
        },
        format: 'DD/MM/YYYY HH:mm',
    })});

    // $("table.blitzTable").on("click", ".blitzTr", function () {
    //     let checkBox = $(this).find("th div input");
    //     checkBox.prop('checked',!checkBox.prop('checked'));
    //     checkBox.change();
    // });
});
