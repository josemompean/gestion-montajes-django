// Esta función se llamará desde la plantilla para inicializar los datos del gráfico
function inicializarDatosGrafico(fechasSemana, montajesSemana, fechasMes, montajesMes, fechasTrimestre, montajesTrimestre) {
    // Datos para los gráficos
    const datosSemanales = {
        labels: fechasSemana,
        datasets: [{
            label: 'Montajes por día',
            data: montajesSemana,
            borderColor: '#2563EB',
            backgroundColor: 'rgba(37, 99, 235, 0.1)',
            borderWidth: 2,
            tension: 0.3,
            fill: true
        }]
    };
    
    const datosMensuales = {
        labels: fechasMes,
        datasets: [{
            label: 'Montajes por día',
            data: montajesMes,
            borderColor: '#2563EB',
            backgroundColor: 'rgba(37, 99, 235, 0.1)',
            borderWidth: 2,
            tension: 0.3,
            fill: true
        }]
    };
    
    const datosTrimestre = {
        labels: fechasTrimestre,
        datasets: [{
            label: 'Montajes por semana',
            data: montajesTrimestre,
            borderColor: '#2563EB',
            backgroundColor: 'rgba(37, 99, 235, 0.1)',
            borderWidth: 2,
            tension: 0.3,
            fill: true
        }]
    };
    
    // Inicializar el gráfico cuando el DOM esté listo
    document.addEventListener('DOMContentLoaded', function() {
        window.inicializarGrafico(datosSemanales, datosMensuales, datosTrimestre);
    });
}
