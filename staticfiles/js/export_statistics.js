function updateExportUrl() {
    const year = $("#year").val();
    $("#exportBtn").attr("href", `/dashboard/export/${year}`);
}

$(document).ready(function() {
    updateExportUrl();
    
    $("#exportBtn").click(function(event) {
        event.preventDefault(); // Prevenir o comportamento padrão do link
        updateExportUrl(); // Atualizar a URL de exportação
        window.location.href = $("#exportBtn").attr("href"); // Redirecionar para a URL de exportação
    });
});

$("#year").change(function() {
    updateExportUrl();
});