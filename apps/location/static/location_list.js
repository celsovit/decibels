    // ao carregar a página
    $(document).ready(function () {

        // ação do botão delete
        $(".delete-btn").click(function () {
            var url = $(this).data("item-url");
            var itemName = $(this).data("item-name");
            $("#itemName").text(itemName);
            $("#confirmDeleteBtn").attr("href", url);
            $("#confirmDeleteModal").modal("show");
        });

        // ação do botão gráfico
        $(".graph-btn").click(function () {
            const locationId = $(this).data("location-id");
            const name = $(this).data('location-name');

            $("#measurementGraphModalLabel").text("Gráfico de Medição :: " + name);
            $("#modalYear").empty();

            $.ajax({
                url: "/location/" + locationId + "/graphic/filter-options",
                type: "GET",
                dataType: "json",
                success: (jsonResponse) => {
                    jsonResponse.options.forEach(option => {
                        $("#modalYear").append(new Option(option, option));
                    });
                    loadLocationChart(locationId, $("#modalYear").children().first().val());
                },
                error: () => console.log("Falha ao obter opções de filtro de gráfico!")
            });

        });

    });

    // ao carregar o modal do gráfico
    $("#measurementGraphModal").on('show.bs.modal', (event) => {
        const button = $(event.relatedTarget);
        const locationId = button.data('location-id');

        // Remove os manipuladores de eventos 'click' anteriores
        $("#loadChartBtn").off('click');

        // ação do botão carregar ano
        $("#loadChartBtn").click(() => {
            const year = $("#modalYear").val();
            loadLocationChart(locationId, year);
        });
    });

    // vincula objeto Chart.js ao canvas (#measurementChart)
    const ctx = document.getElementById("measurementChart").getContext("2d");
    const chart = new Chart(ctx, {
        type: "line",
        options: {
            responsive: true,
            title: {
                display: false,
                text: ""
            }
        }
    });

    // construção do gráfico
    function loadLocationChart(locationId, year) {
        if (year === undefined) return;

        const endpoint = "/location/" + locationId + "/graphic/" + year;
        $.ajax({
            url: endpoint,
            type: "GET",
            dataType: "json",
            success: (jsonResponse) => {
                
                const title = jsonResponse.title;
                const labels = jsonResponse.data.labels;
                const datasets = jsonResponse.data.datasets;

                chart.data.datasets = [];
                chart.data.labels = [];

                chart.options.title.text = title;
                chart.options.title.display = true;
                chart.data.labels = labels;
                datasets.forEach(dataset => {
                    chart.data.datasets.push(dataset);
                });
                chart.update();

            },
            error: () => console.log("Failed to fetch chart data from " + endpoint + "!")
        });
    }
